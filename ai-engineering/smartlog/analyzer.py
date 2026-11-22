"""Deterministic, offline log-quality analysis. No network or AI calls."""

from collections import Counter, defaultdict
from datetime import datetime, timezone
import re

from parsers import is_continuation, load_rules, parse_timestamp, parse_with, select_parsers

MAX_BYTES = 5 * 1024 * 1024
MAX_LINES = 50_000
ERROR_LEVELS = {"ERROR", "FATAL", "CRITICAL"}
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




def parse_line_detail(line: str, parsers=None) -> tuple[dict | None, str]:
    """Parse a line and return a safe diagnostic category, never raw content."""
    raw = line.strip().lstrip("\ufeff")
    if not raw:
        return None, "blank"
    record, reason = parse_with(parsers if parsers is not None else select_parsers(), raw)
    if record is None:
        return None, reason
    return {"timestamp": record.timestamp, "level": record.level,
            "message": record.message, "format": record.format}, "parsed"


def parse_line(line: str) -> dict | None:
    """Compatibility helper for callers needing only a parsed record."""
    return parse_line_detail(line)[0]


def analyze(text: str, start: datetime | None = None, end: datetime | None = None,
            burst_seconds: int = 30, burst_threshold: int = 3,
            parser: str = "auto", rules_text: str | None = None) -> dict:
    """Return JSON-serializable statistics, never raw log messages.

    ``parser`` selects "auto" or one named parser. ``rules_text`` holds optional
    JSON regex rules for application-specific formats (see parsers.load_rules).
    """
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
    rules = load_rules(rules_text) if rules_text and rules_text.strip() else ()
    parsers = select_parsers(parser, rules=rules)

    levels = Counter()
    patterns = defaultdict(lambda: {"count": 0, "bytes": 0})
    bursts = Counter()
    invalid = matched = ignored = matched_bytes = 0
    blank = continuation = 0
    parse_failures = Counter()
    formats = Counter()
    earliest = latest = None
    attachable = False  # True once any non-blank line precedes the current one
    for line in lines:
        if not line.strip():
            blank += 1
            continue
        if attachable and is_continuation(line):
            # Multiline payload belongs to the preceding line (parsed or not); it is
            # counted separately rather than as a parse failure, and never discarded.
            continuation += 1
            continue
        attachable = True
        record, reason = parse_line_detail(line, parsers)
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
    considered = len(lines) - blank
    handled = matched + ignored + continuation
    unsupported = parse_failures.get("unsupported_prefix", 0)
    return {
        "input_lines": len(lines), "blank_lines": blank,
        "matched_lines": matched, "invalid_lines": invalid,
        "unsupported_lines": unsupported, "malformed_lines": invalid - unsupported,
        "continuation_lines": continuation,
        "parse_failures": dict(sorted(parse_failures.items())),
        "detected_formats": dict(sorted(formats.items())),
        "detected_format": formats.most_common(1)[0][0] if formats else None,
        "parser": parser,
        "parse_success_percent": round(100 * handled / considered, 2) if considered else 0,
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
        f"- Total input lines: {result['input_lines']:,}",
        f"- Blank lines: {result['blank_lines']:,}",
        f"- Parsed logs: {result['matched_lines']:,}",
        f"- Continuation lines (attached to parsed records): {result['continuation_lines']:,}",
        f"- Unparsed lines: {result['invalid_lines']:,} (unsupported: {result['unsupported_lines']:,}, malformed: {result['malformed_lines']:,})",
        f"- Skipped (outside selected time range): {result['outside_time_range']:,}",
        f"- Parsing success: {result['parse_success_percent']}%",
        f"- Parser selection: {result['parser']}",
        f"- Detected format: {result['detected_format']}",
        f"- Detected formats: {result['detected_formats']}",
        f"- Safe parsing failure counts: {result['parse_failures']}",
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
