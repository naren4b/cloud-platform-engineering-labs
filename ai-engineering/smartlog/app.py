"""Streamlit front end for the offline SmartLog v0.1 analyzer."""

from datetime import datetime, time, timezone
import csv
from io import StringIO
import json
from pathlib import Path

import streamlit as st

from analyzer import MAX_BYTES, analyze, to_markdown
from parsers import AUTO, BUILTIN_PARSER_NAMES

st.set_page_config(page_title="SmartLog", page_icon="📋", layout="wide")
st.title("SmartLog: Logging Quality Analyzer")
st.caption("Offline v0.1.1. Paste or upload logs. No LLM, Loki connection, or outbound API calls.")

source = st.radio("Source", ["Paste logs", "Upload log file", "Synthetic demo"], horizontal=True)
parser_name = st.selectbox(
    "Log format",
    [AUTO, *BUILTIN_PARSER_NAMES],
    help="Auto tries every supported format. Pick one manually if detection fails.",
)
rules_text = None
with st.expander("Custom parser rules (optional JSON, kept on this machine)"):
    rules_upload = st.file_uploader("Parser rules file", type=["json"], key="rules")
    if rules_upload is not None:
        rules_text = rules_upload.getvalue().decode("utf-8", errors="replace")
log_text = ""
if source == "Paste logs":
    log_text = st.text_area("Log lines", height=220, placeholder="2026-06-27 10:00:00 INFO Service started")
elif source == "Upload log file":
    uploaded = st.file_uploader("Choose .txt, .log or .jsonl", type=["txt", "log", "jsonl"])
    if uploaded is not None:
        raw = uploaded.getvalue()
        if len(raw) > MAX_BYTES:
            st.error("Upload exceeds the 5 MiB safety limit")
            st.stop()
        log_text = raw.decode("utf-8", errors="replace")
else:
    log_text = (Path(__file__).parent / "samples" / "sample.log").read_text(encoding="utf-8")
    st.info("Using bundled synthetic logs, no production data.")

if log_text.strip():
    try:
        initial = analyze(log_text, parser=parser_name, rules_text=rules_text)
        start = end = None
        if initial["coverage_start_utc"]:
            lower = datetime.fromisoformat(initial["coverage_start_utc"]).date()
            upper = datetime.fromisoformat(initial["coverage_end_utc"]).date()
            if st.checkbox("Filter by UTC date", value=False):
                chosen = st.date_input("Date range (UTC)", value=(lower, upper), min_value=lower, max_value=upper)
                if len(chosen) == 2:
                    start = datetime.combine(chosen[0], time.min, tzinfo=timezone.utc)
                    end = datetime.combine(chosen[1], time.max, tzinfo=timezone.utc)
                else:
                    st.warning("Choose a start and end date")
                    st.stop()
        result = analyze(log_text, start=start, end=end, parser=parser_name, rules_text=rules_text)
    except ValueError as error:
        st.error(str(error))
        st.stop()

    a, b, c, d = st.columns(4)
    a.metric("Total input lines", f"{result['input_lines']:,}")
    b.metric("Parsed logs", f"{result['matched_lines']:,}")
    c.metric("Skipped (time range)", f"{result['outside_time_range']:,}")
    d.metric("Unparsed lines", f"{result['invalid_lines']:,}")
    e, f, g = st.columns(3)
    e.metric("Unsupported lines", f"{result['unsupported_lines']:,}")
    f.metric("Malformed lines", f"{result['malformed_lines']:,}")
    g.metric("Continuation lines", f"{result['continuation_lines']:,}")
    st.caption(f"Parsing success: {result['parse_success_percent']}% | "
               f"Detected format: {result['detected_format'] or 'none'} | "
               f"Parser: {result['parser']} | Blank lines: {result['blank_lines']:,}")
    if result["invalid_lines"]:
        with st.expander("Parsing diagnostics (counts only, no raw log samples)"):
            st.json(result["parse_failures"])
            st.caption("Unparsed lines are never discarded from the source file. "
                       "Use the Log format selector or a rules file if detection fails.")

    if result["matched_lines"] == 0:
        if result["outside_time_range"]:
            st.warning("No records fall inside the selected time range.")
        else:
            st.warning("No matching log format detected.")
        st.write("SmartLog accepts logfmt/logrus (time=… level=… msg=…), ISO timestamp-first text, "
                 "Kubernetes CRI, and JSON/JSONL records. Choose a format manually or add a rules file.")
        st.download_button(
            "Download safe parsing summary",
            json.dumps({
                "input_lines": result["input_lines"],
                "blank_lines": result["blank_lines"],
                "parsed_lines": result["matched_lines"],
                "skipped_lines": result["outside_time_range"],
                "unparsed_lines": result["invalid_lines"],
                "unsupported_lines": result["unsupported_lines"],
                "malformed_lines": result["malformed_lines"],
                "continuation_lines": result["continuation_lines"],
                "parser": result["parser"],
                "parse_failures": result["parse_failures"],
                "detected_formats": result["detected_formats"],
            }, indent=2),
            "smartlog-parsing-diagnostics.json", "application/json",
        )
    else:
        st.caption(f"Approx. bytes: {result['approx_bytes']:,} | "
                   f"Unique templates: {result['unique_templates']:,}")
        st.subheader("Severity distribution")
        if result["levels"]:
            st.bar_chart(
                [{"level": level, "count": count}
                 for level, count in result["levels"].items()],
                x="level", y="count",
            )
        else:
            st.info("No severity data available for the selected time range.")

        st.subheader("Top log patterns by byte volume")
        if result["patterns"]:
            st.dataframe(result["patterns"][:10], use_container_width=True, hide_index=True)
        else:
            st.info("No log patterns found.")
        st.subheader("Error bursts (more than 3 ERROR/FATAL/CRITICAL events per 30 seconds)")
        if result["error_bursts"]:
            st.dataframe(result["error_bursts"], use_container_width=True, hide_index=True)
        else:
            st.info("No error bursts above the configured threshold.")
        st.caption(result["note"])

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["level", "template", "count", "bytes", "percent"])
        writer.writeheader()
        writer.writerows(result["patterns"])
        col1, col2, col3 = st.columns(3)
        col1.download_button("Download Markdown", to_markdown(result), "smartlog-report.md", "text/markdown")
        col2.download_button("Download JSON", json.dumps(result, indent=2), "smartlog-report.json", "application/json")
        col3.download_button("Download patterns CSV", output.getvalue(), "smartlog-patterns.csv", "text/csv")
else:
    st.info("Paste logs, upload a file, or select the synthetic demo to start.")
