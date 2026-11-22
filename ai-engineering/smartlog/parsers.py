"""Pluggable, offline log-line parsers.

Each parser turns one line into a Record, or returns a safe reason code that
never contains raw log content. Auto mode tries parsers in order for every
line; manual mode uses one parser. New formats are added by subclassing
LineParser or by a JSON rule (see load_rules); the analysis engine is unchanged.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import re

AUTO = "auto"
NO_MATCH = "no_match"
LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "FATAL", "CRITICAL", "UNKNOWN"}
LEVEL_TOKEN = re.compile(r"\b(TRACE|DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\b", re.I)
# Continuation lines: indented stack frames, "Caused by:" and "... N more" markers.
CONTINUATION = re.compile(r"^(?:\s|[}\]\"]|Caused by:|\.\.\.\s*\d+\s+more\b)")

# Common timestamp-first logs, optional brackets and nanosecond fractions.
ISO_TS = (r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}"
          r"(?:[.,]\d{1,9})?(?:Z|[+-]\d{2}:?\d{2})?")
TS_FIRST = re.compile(rf"^\[?(?P<timestamp>{ISO_TS})\]?\s+(?P<body>.+)$")
CRI_LINE = re.compile(
    rf"^(?P<timestamp>{ISO_TS})\s+(?:stdout|stderr)\s+[FP]\s+(?P<body>.*)$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Record:
    timestamp: datetime
    level: str
    message: str
    format: str


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


def normalize_level(value: str) -> str:
    level = str(value).strip().upper()
    if level == "WARNING":
        return "WARN"
    return level if level in LEVELS else "UNKNOWN"


def _severity_and_message(body: str) -> tuple[str, str]:
    """Find a severity token near the start, otherwise mark UNKNOWN."""
    match = LEVEL_TOKEN.search(body[:120])
    if match is None:
        return "UNKNOWN", body.strip()
    level = normalize_level(match.group(1))
    # Keep logger and thread metadata intact; discard only the severity token.
    message = (body[:match.start()] + " " + body[match.end():]).strip(" \t-:|[]")
    return level, (message or body.strip())


def _build_text_record(timestamp: str, body: str, format_name: str) -> tuple[Record | None, str]:
    stamp = parse_timestamp(timestamp)
    if stamp is None:
        return None, "invalid_timestamp"
    if not body.strip():
        return None, "missing_message"
    level, message = _severity_and_message(body)
    return Record(stamp, level, message, format_name), ""


class LineParser(ABC):
    """Parses one stripped line. Returns (record, "") or (None, safe_reason)."""

    name: str

    @abstractmethod
    def parse(self, raw: str) -> tuple[Record | None, str]:
        """Return a parsed record, or a reason code that never echoes log content."""


class JsonLineParser(LineParser):
    """JSON objects, including Docker json-file envelopes with a `log` key."""

    name = "jsonl"

    def parse(self, raw: str) -> tuple[Record | None, str]:
        if not raw.startswith("{"):
            return None, NO_MATCH
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
        else:
            inferred = normalize_level(level)
        return Record(stamp, inferred, message, self.name), ""


class KubernetesCriParser(LineParser):
    """Container runtime (CRI) lines: `<ts> stdout|stderr F|P <payload>`."""

    name = "kubernetes-cri"

    def parse(self, raw: str) -> tuple[Record | None, str]:
        match = CRI_LINE.match(raw)
        if match is None:
            return None, NO_MATCH
        timestamp, body = match.group("timestamp", "body")
        # Many CRI lines contain an application timestamp inside the payload.
        inner = TS_FIRST.match(body.strip())
        if inner:
            timestamp, body = inner.group("timestamp", "body")
        return _build_text_record(timestamp, body, self.name)


class TimestampTextParser(LineParser):
    """Timestamp-first text lines with optional severity and logger metadata."""

    name = "text"

    def parse(self, raw: str) -> tuple[Record | None, str]:
        match = TS_FIRST.match(raw)
        if match is None:
            return None, NO_MATCH
        return _build_text_record(match.group("timestamp"), match.group("body"), self.name)


LOGFMT_PAIR = re.compile(r'([A-Za-z_][\w.-]*)=("(?:[^"\\]|\\.)*"|\S*)')


class LogfmtParser(LineParser):
    """logfmt / logrus key=value records: `time=... level=... msg=... key=value`."""

    name = "logfmt"

    def parse(self, raw: str) -> tuple[Record | None, str]:
        pairs = {key: _unquote(value) for key, value in LOGFMT_PAIR.findall(raw)}
        if "time" not in pairs and "msg" not in pairs:
            return None, NO_MATCH
        if "time" not in pairs:
            return None, "missing_timestamp"
        if "msg" not in pairs:
            return None, "missing_message"
        stamp = parse_timestamp(pairs["time"])
        if stamp is None:
            return None, "invalid_timestamp"
        message = pairs["msg"].strip()
        if not message:
            return None, "missing_message"
        level = normalize_level(pairs["level"]) if pairs.get("level") else "UNKNOWN"
        return Record(stamp, level, message, self.name), ""


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


BUILTIN_PARSER_NAMES = ("jsonl", "logfmt", "kubernetes-cri", "text")
RESERVED_NAMES = frozenset({AUTO, *BUILTIN_PARSER_NAMES})
BUILTIN_PARSERS: tuple[LineParser, ...] = (
    JsonLineParser(), LogfmtParser(), KubernetesCriParser(), TimestampTextParser(),
)

_RULE_KEYS = {"name", "pattern", "timestamp_format", "level_aliases"}


class RegexRuleParser(LineParser):
    """Application-specific format described by a regex with named groups.

    Required groups: `timestamp` and `message`. Optional group: `level`.
    `timestamp_format` is a strptime pattern; without it ISO 8601 or epoch is used.
    """

    def __init__(self, name: str = "", pattern: str = "", timestamp_format: str | None = None,
                 level_aliases: dict | None = None):
        if not name or not isinstance(name, str):
            raise ValueError("Each parser rule needs a non-empty name")
        if name in RESERVED_NAMES:
            raise ValueError(f"Rule name '{name}' is reserved")
        if not pattern or not isinstance(pattern, str):
            raise ValueError(f"Rule '{name}' needs a regex pattern")
        try:
            compiled = re.compile(pattern)
        except re.error as error:
            raise ValueError(f"Rule '{name}' has an invalid regex: {error}") from None
        missing = {"timestamp", "message"} - set(compiled.groupindex)
        if missing:
            raise ValueError(f"Rule '{name}' must define named groups: {', '.join(sorted(missing))}")
        if timestamp_format is not None and not isinstance(timestamp_format, str):
            raise ValueError(f"Rule '{name}' timestamp_format must be a string")
        aliases = level_aliases or {}
        if not isinstance(aliases, dict):
            raise ValueError(f"Rule '{name}' level_aliases must be an object")
        self.name = name
        self._pattern = compiled
        self._timestamp_format = timestamp_format
        self._aliases = {str(k).upper(): str(v) for k, v in aliases.items()}

    def parse(self, raw: str) -> tuple[Record | None, str]:
        match = self._pattern.match(raw)
        if match is None:
            return None, NO_MATCH
        stamp = self._timestamp(match.group("timestamp"))
        if stamp is None:
            return None, "invalid_timestamp"
        message = (match.group("message") or "").strip()
        if not message:
            return None, "missing_message"
        raw_level = match.group("level") if "level" in self._pattern.groupindex else None
        level = normalize_level(self._aliases.get(raw_level.upper(), raw_level)) if raw_level else "UNKNOWN"
        return Record(stamp, level, message, self.name), ""

    def _timestamp(self, text: str) -> datetime | None:
        if self._timestamp_format is None:
            return parse_timestamp(text)
        try:
            stamp = datetime.strptime(text.strip(), self._timestamp_format)
        except ValueError:
            return None
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        return stamp.astimezone(timezone.utc)


def load_rules(text: str) -> list[RegexRuleParser]:
    """Load application rules from JSON: {"rules": [...]} or a bare list."""
    if not text or not text.strip():
        return []
    try:
        document = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(f"Rules file is not valid JSON (line {error.lineno})") from None
    items = document.get("rules") if isinstance(document, dict) else document
    if not isinstance(items, list):
        raise ValueError('Rules must be a list or an object with a "rules" list')
    rules = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each parser rule must be a JSON object")
        unknown = set(item) - _RULE_KEYS
        if unknown:
            raise ValueError(f"Unknown parser rule keys: {', '.join(sorted(unknown))}")
        rules.append(RegexRuleParser(**item))
    names = [rule.name for rule in rules]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(f"Duplicate parser rule names: {', '.join(duplicates)}")
    return rules


def select_parsers(selection: str = AUTO, rules=()) -> list[LineParser]:
    """Auto returns every parser (custom rules first). A name returns only that parser."""
    candidates = [*rules, *BUILTIN_PARSERS]
    if selection in (None, "", AUTO):
        return candidates
    for parser in candidates:
        if parser.name == selection:
            return [parser]
    raise ValueError(f"Unknown parser '{selection}'")


def parse_with(parsers, raw: str) -> tuple[Record | None, str]:
    """Return the first successful parse, else the most specific safe reason."""
    reasons = []
    for parser in parsers:
        record, reason = parser.parse(raw)
        if record is not None:
            return record, ""
        reasons.append(reason)
    for reason in reasons:
        if reason != NO_MATCH:
            return None, reason
    return None, "unsupported_prefix"


def is_continuation(line: str) -> bool:
    return bool(CONTINUATION.match(line))
