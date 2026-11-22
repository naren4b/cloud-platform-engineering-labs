"""Offline, explainable log-noise review and a prompt without raw log messages."""

import re

PROTECTED_LEVELS = {"ERROR", "FATAL", "CRITICAL"}
PROTECTED_TERMS = re.compile(r"\b(audit|security|authentication|authorization|access.denied)\b", re.I)


def find_candidates(report, min_count=3, min_share=10.0, limit=20):
    """Rank noisy-pattern candidates. None is ever classified safe to delete."""
    total = report.get("matched_lines", 0)
    total_bytes = report.get("approx_bytes", 0)
    if not total:
        return []
    findings = []
    for rank, row in enumerate(report.get("patterns", [])[:limit], 1):
        level = row["level"].upper()
        count, size = row["count"], row["bytes"]
        count_share = 100 * count / total
        byte_share = 100 * size / total_bytes if total_bytes else 0
        heavy = count >= min_count and max(count_share, byte_share) >= min_share
        protected = level in PROTECTED_LEVELS or bool(PROTECTED_TERMS.search(row["template"]))
        if protected:
            action, rationale = "PROTECTED", "Preserve audit, security and failure evidence."
        elif level == "UNKNOWN":
            action, rationale = "REVIEW_FORMAT", "Verify missing severity before tuning."
        elif level == "WARN" and heavy:
            action, rationale = "INVESTIGATE", "Repeated warnings may indicate real failures."
        elif heavy and level in {"INFO", "DEBUG", "TRACE"}:
            action, rationale = "REVIEW_REDUCE", "Repeated low-severity pattern has material volume."
        else:
            action, rationale = "KEEP", "Insufficient evidence for a logging change."
        findings.append({
            "id": f"pattern-{rank}", "level": level,
            "template": row["template"], "count": count, "bytes": size,
            "event_share_percent": round(count_share, 2),
            "byte_share_percent": round(byte_share, 2),
            "action": action, "protected": protected, "reason": rationale,
            "confidence": "LOW",
        })
    return findings


def next_action_prompt(report, findings):
    """Generate step-by-step follow-up without any raw templates or source names."""
    lines = [
        "# SmartLog Next Action", "",
        "Use only an approved local developer environment.",
        "Never upload production logs, proprietary code or internal identifiers.",
        "This prompt excludes log message templates, but aggregate counts may",
        "still be confidential. Do not share it outside the approved environment.",
        "",
        f"Parsed events: {report.get('matched_lines', 0)}",
        f"Unparsed lines: {report.get('invalid_lines', 0)}",
        "",
    ]
    if not report.get("matched_lines"):
        lines += [
            "## First action: fix parser coverage",
            "Inspect format locally; create an invented synthetic fixture.",
            "Add a parser adapter and verify no unsupported lines are silently ignored.",
        ]
    else:
        noise = next((f for f in findings if f["action"] == "REVIEW_REDUCE"), None)
        protected = any(f["action"] in {"PROTECTED", "INVESTIGATE"} for f in findings)
        if noise is not None:
            lines += [
                "## First action: review repeated logging",
                f"Finding ID: {noise['id']}",
                f"Severity: {noise['level']}",
                f"Events: {noise['count']}",
                f"Approximate byte share: {noise['byte_share_percent']}%",
                "Find the logging callsite using the local detailed report.",
                "Consider keeping, reducing, aggregating, changing level, or",
                "replacing with a metric. Explain the diagnostic risk.",
                "Never suppress security, audit, or critical failures.",
            ]
        elif protected:
            lines += [
                "## First action: investigate protected and failing events",
                "Find the root cause. High error frequency is not harmless noise.",
                "Preserve the evidence and request service-owner review.",
            ]
        else:
            lines += [
                "## First action: improve the baseline",
                "Compare representative time windows. No strong candidate was found.",
            ]
        if report.get("invalid_lines"):
            lines += ["", "Follow-up: fix parsing gaps before trusting volume coverage."]
    lines += [
        "", "## Deliverables",
        "1. Finding evidence and assumptions.",
        "2. Diagnostic, security and compliance impact.",
        "3. Smallest source-code or observability change to review.",
        "4. Synthetic regression tests.",
        "5. Before/after evaluation plan.",
        "", "Do not apply any production changes automatically.",
    ]
    return "\n".join(lines) + "\n"
