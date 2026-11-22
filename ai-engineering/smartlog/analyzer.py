"""Deterministic, offline log-quality analysis. No network or AI calls."""

from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import re

MAX_BYTES = 5 * 1024 * 1024
MAX_LINES = 50_000
LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "FATAL", "CRITICAL"}
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


def parse_timestamp(value) -> datetime | None:
    if value is None:
        return None
    try:
        stamp = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00").replace(",", "."))
    except ValueError:
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(timezone.utc)


def parse_line(line: str) -> dict | None:
    raw = line.strip()
    if not raw:
        return None
    if raw.startswith("{"):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            return None
        if not isinstance(value, dict):
            return None
        timestamp = next((value.get(k) for k in ("timestamp", "time", "ts") if value.get(k) is not None), None)
        level = next((value.get(k) for k in ("level", "severity", "log_level") if value.get(k) is not None), None)
        message = next((value.get(k) for k in ("message", "msg", "log") if value.get(k) is not None), None)
    else:
        match = TEXT_LINE.match(raw)
        if not match:
            return None
        timestamp, level, message = match.group("timestamp", "level", "message")
    stamp = parse_timestamp(timestamp)
    if stamp is None or level is None or message is None:
        return None
    level = str(level).upper()
    if level not in LEVELS:
        return None
    return {"timestamp": stamp, "level": "WARN" if level == "WARNING" else level, "message": str(message)}


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
    earliest = latest = None
    for line in lines:
        record = parse_line(line)
        if record is None:
            invalid += 1
            continue
        when = record["timestamp"]
        if (start and when < start) or (end and when > end):
            ignored += 1
            continue
        matched += 1
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
