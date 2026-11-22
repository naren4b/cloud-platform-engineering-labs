"""Deterministic, offline log-quality analysis. No network or AI calls."""

from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import re

MAX_BYTES = 5 * 1024 * 1024
MAX_LINES = 50_000
LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "FATAL", "CRITICAL", "UNKNOWN"}
ERROR_LEVELS = {"ERROR", "FATAL", "CRITICAL"}
TEXT_LINE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?(?:Z|[+-]\d{2}:?\d{2})?)\s+"
    r"(?P<level>TRACE|DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\s+(?P<message>.+)$",
    re.IGNORECASE,
)
SENSITIVE = re.compile(
    r"(?i)\b(password|passwd|token|secret|api[_-]?key|authorization)\s*[:=]\s*(?:\"[^\"]*\"|'[^']*'|\S+)"
)
REPLACEMENTS = [
    (re.compile(r"(?i)\bbearer\s+\S+"), "<credential>"),
    (re.compile(r"https?://\S+", re.I), "<url>"),
    (re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"), "<email>"),
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "<ip>"),
    (re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"), "<uuid>"),
    (re.compile(r"\b(?:0x)?[0-9a-fA-F]{24,}\b"), "<hex>"),
    (re.compile(r"\b\d+(?:\.\d+)?\b"), "<num>"),
]


def normalize_message(message: str) -> str:
    """Group variable values; best-effort redaction, not a DLP guarantee."""
    value = SENSITIVE.sub(lambda m: f"{m.group(1)}=<redacted>", message)
    for pattern, replacement in REPLACEMENTS:
        value = pattern.sub(replacement, value)
    return " ".join(value.split())[:240]


# Common timestamp-first logs, optional brackets and nanosecond fractions.
ISO_TS = (r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}"
          r"(?:[.,]\d{1,9})?(?:Z|[+-]\d{2}:?\d{2})?")
TS_FIRST = re.compile(rf"^\[?(?P<timestamp>{ISO_TS})\]?\s+(?P<body>.+)$")
CRI_LINE = re.compile(
    rf"^(?P<timestamp>{ISO_TS})\s+(?:stdout|stderr)\s+[FP]\s+(?P<body>.*)$",
    re.IGNORECASE,
)
LEVEL_TOKEN = re.compile(r"\b(TRACE|DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\b", re.I)


def parse_timestamp(value) -> datetime | None:
    """Parse ISO 8601 or Unix epochs. Timestamps without a zone mean UTC."""
    if value is None:
        return None
    try:
        if isinstance(value, (int, float)) or (
            isinstance(value, str) and re.fullmatch(r"\d{10,19}", value.strip())
        ):
            number = float(value)
            while number > 4_102_444_800:
                number /= 1000
            if not 946_684_800 <= number <= 4_102_444_800:
                return None
            return datetime.fromtimestamp(number, tz=timezone.utc)
        stamp = datetime.fromisoformat(
            str(value).strip().replace("Z", "+00:00").replace(",", ".")
        )
    except (ValueError, TypeError, OverflowError, OSError):
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(timezone.utc)


def _severity_and_message(body: str) -> tuple[str, str]:
    """Find a severity token near the start, otherwise mark UNKNOWN."""
    match = LEVEL_TOKEN.search(body[:120])
    if match is None:
        return "UNKNOWN", body.strip()
    level = match.group(1).upper()
    if level == "WARNING":
        level = "WARN"
    # Keep logger and thread metadata intact; discard only the severity token.
    message = (body[:match.start()] + " " + body[match.end():]).strip(" \t-:|[]")
    return level, (message or body.strip())


def parse_line_detail(line: str) -> tuple[dict | None, str]:
    """Parse a line and return a safe diagnostic category, never raw content."""
    raw = line.strip().lstrip("\ufeff")
    if not raw:
        return None, "blank"
    if raw.startswith("{"):
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            return None, "invalid_json"
        if not isinstance(obj, dict):
            return None, "unsupported_json"
        timestamp = next((obj[k] for k in ("timestamp", "time", "ts", "@timestamp")
                          if obj.get(k) is not None), None)
        message = next((obj[k] for k in ("message", "msg", "log")
                        if obj.get(k) is not None), None)
        level = next((obj[k] for k in ("level", "severity", "log_level")
                      if obj.get(k) is not None), None)
        if timestamp is None:
            return None, "missing_timestamp"
        if message is None:
            return None, "missing_message"
        stamp = parse_timestamp(timestamp)
        if stamp is None:
            return None, "invalid_timestamp"
        if isinstance(message, (dict, list)):
            message = json.dumps(message, ensure_ascii=False)
        message = str(message).strip()
        if not message:
            return None, "missing_message"
        if level is None:
            inferred, message = _severity_and_message(message)
            level = inferred
        else:
            level = str(level).upper()
            level = "WARN" if level == "WARNING" else level
            if level not in LEVELS:
                level = "UNKNOWN"
        return {"timestamp": stamp, "level": level, "message": message,
                "format": "jsonl"}, "parsed"

    format_name = "text"
    match = CRI_LINE.match(raw)
    if match:
        format_name = "kubernetes-cri"
        timestamp = match.group("timestamp")
        body = match.group("body")
        # Many CRI lines contain an application timestamp inside the payload.
        inner = TS_FIRST.match(body.strip())
        if inner:
            timestamp, body = inner.group("timestamp", "body")
    else:
        match = TS_FIRST.match(raw)
        if match is None:
            return None, "unsupported_prefix"
        timestamp, body = match.group("timestamp", "body")
    stamp = parse_timestamp(timestamp)
    if stamp is None:
        return None, "invalid_timestamp"
    if not body.strip():
        return None, "missing_message"
    level, message = _severity_and_message(body)
    return {"timestamp": stamp, "level": level, "message": message,
            "format": format_name}, "parsed"


def parse_line(line: str) -> dict | None:
    """Compatibility helper for callers needing only a parsed record."""
    return parse_line_detail(line)[0]


def analyze(text: str, start: datetime | None = None, end: datetime | None = None,
            burst_seconds: int = 30, burst_threshold: int = 3) -> dict:
    """Return JSON-serializable statistics, never raw log messages."""
    if len(text.encode("utf-8")) > MAX_BYTES:
        raise ValueError("Input exceeds the 5 MiB safety limit")
    lines = text.splitlines()
    if len(lines) > MAX_LINES:
        raise ValueError("Input exceeds the 50,000-line safety limit")
    if burst_seconds <= 0 or burst_threshold < 0:
        raise ValueError("Invalid error-burst settings")
    if start is not None and start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end is not None and end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    if start and end and start > end:
        raise ValueError("Start must not be after end")

    levels = Counter()
    patterns = defaultdict(lambda: {"count": 0, "bytes": 0})
    bursts = Counter()
    invalid = matched = ignored = matched_bytes = 0
    parse_failures = Counter()
    formats = Counter()
    earliest = latest = None
    for line in lines:
        record, reason = parse_line_detail(line)
        if record is None:
            invalid += 1
            parse_failures[reason] += 1
            continue
        when = record["timestamp"]
        if (start and when < start) or (end and when > end):
            ignored += 1
            continue
        matched += 1
        formats[record["format"]] += 1
        approx_bytes = len(line.encode("utf-8")) + 1
        matched_bytes += approx_bytes
        levels[record["level"]] += 1
        normalized = normalize_message(record["message"])
        key = (record["level"], normalized)
        patterns[key]["count"] += 1
        patterns[key]["bytes"] += approx_bytes
        earliest = min(earliest, when) if earliest else when
        latest = max(latest, when) if latest else when
        if record["level"] in ERROR_LEVELS:
            window = int(when.timestamp()) // burst_seconds * burst_seconds
            bursts[window] += 1

    grouped = [
        {"level": level, "template": template, "count": values["count"],
         "bytes": values["bytes"], "percent": round(100 * values["count"] / matched, 2)}
        for (level, template), values in patterns.items()
    ]
    grouped.sort(key=lambda r: (-r["bytes"], -r["count"], r["level"], r["template"]))
    suspicious_windows = [
        {"window_utc": datetime.fromtimestamp(window, timezone.utc).isoformat(), "error_count": count}
        for window, count in bursts.items() if count > burst_threshold
    ]
    suspicious_windows.sort(key=lambda r: (-r["error_count"], r["window_utc"]))
    return {
        "input_lines": len(lines), "matched_lines": matched, "invalid_lines": invalid,
        "parse_failures": dict(sorted(parse_failures.items())),
        "detected_formats": dict(sorted(formats.items())),
        "parse_success_percent": round(100 * (matched + ignored) / len(lines), 2) if lines else 0,
        "outside_time_range": ignored, "approx_bytes": matched_bytes,
        "levels": dict(sorted(levels.items())), "unique_templates": len(grouped),
        "patterns": grouped, "error_bursts": suspicious_windows[:20],
        "coverage_start_utc": earliest.isoformat() if earliest else None,
        "coverage_end_utc": latest.isoformat() if latest else None,
        "complete": True, "note": "Approximate bytes include one newline per selected log line. Patterns use best-effort redaction; review exports before sharing.",
    }


def to_markdown(result: dict) -> str:
    """Create an aggregate-only report suitable for human review."""
    lines = [
        "# SmartLog Quality Report", "",
        f"- Parsed logs: {result['matched_lines']:,}",
        f"- Invalid/unparsed lines: {result['invalid_lines']:,}",
        f"- Parsing success: {result['parse_success_percent']}%",
        f"- Detected formats: {result['detected_formats']}",
        f"- Safe parsing failure counts: {result['parse_failures']}",
        f"- Outside selected time range: {result['outside_time_range']:,}",
        f"- Approximate log bytes: {result['approx_bytes']:,}",
        f"- Unique level/template pairs: {result['unique_templates']:,}",
        f"- First timestamp (UTC): {result['coverage_start_utc']}",
        f"- Last timestamp (UTC): {result['coverage_end_utc']}", "",
        "## Severity distribution", "",
    ]
    for level, count in result["levels"].items():
        lines.append(f"- {level}: {count:,}")
    lines.extend(["", "## Top repeated patterns (by approximate bytes)", ""])
    for item in result["patterns"][:10]:
        lines.append(f"- {item['level']}: {item['template']} | count={item['count']} | bytes={item['bytes']} | {item['percent']}%")
    lines.extend(["", "## Error bursts (top 20)", ""])
    for item in result["error_bursts"]:
        lines.append(f"- {item['window_utc']}: {item['error_count']} events")
    if not result["error_bursts"]:
        lines.append("- None above threshold")
    lines.extend(["", "## Interpretation", "", "Repeated messages are noise candidates, not automatically safe to drop.",
                  "Preserve diagnostic, security and audit logs until reviewed by a service owner.",
                  "This report cannot diagnose missing Loki logs or prove production storage savings.",
                  "", result["note"], ""])
    return "\n".join(lines)
