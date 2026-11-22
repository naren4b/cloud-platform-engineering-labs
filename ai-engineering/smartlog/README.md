# SmartLog: Log Quality Analyzer

**Status:** v0.1 MVP, offline synthetic-data demo.

SmartLog is a lightweight Python log-analysis lab. It helps developers find frequent log patterns, identify ERROR bursts, measure severity and approximate log bytes, and create review packs for source-code improvements. **It does not automatically decide which logs to delete.**

## Architecture

~~~mermaid
flowchart LR
    A[Paste / upload / demo] --> B[Offline parser]
    B --> C[Template grouping and statistics]
    C --> D[Streamlit dashboard]
    C --> E[Markdown / JSON / CSV reports]
    E --> F[Developer review in Cursor]
~~~

## Run locally

~~~bash
cd ai-engineering/smartlog
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
~~~

Open the local Streamlit URL shown in the terminal. Select **Synthetic demo** to explore without adding data.

~~~bash
python -m unittest discover -s tests -v
~~~

## Run with Docker

~~~bash
cd ai-engineering/smartlog
docker build -t smartlog:0.1 .
docker run --rm -p 127.0.0.1:8501:8501 smartlog:0.1
~~~

## v0.1 features

- Paste or upload .txt, .log, or .jsonl, or use bundled synthetic logs.
- Parse timestamps, severity and message from YYYY-MM-DD HH:MM:SS LEVEL message or JSONL with timestamp/time/ts, level/severity, and message/msg.
- Filter logs by UTC date; timestamps without a timezone are interpreted as UTC.
- Show severity counts, top normalized message templates, approximate bytes, and fixed 30-second ERROR bursts.
- Download aggregate-only Markdown, JSON and CSV reports suitable for developer review.
- Cap input at 5 MiB and 50,000 lines to limit resource use.

## Quality and privacy boundaries

- The app makes **no outbound application/LLM API calls** and does not store user input itself. Streamlit usage telemetry is disabled.
- Uploaded logs are held in the Streamlit process memory. The hosting environment still needs access controls and retention review.
- Reports contain normalized templates, not raw log lines. Redaction is **best-effort, not guaranteed DLP**: treat all production inputs and exports as sensitive until independently reviewed.
- Raw or corporate production logs and credentials must not be committed to this public repository or sent to unapproved AI tools.
- High-volume patterns are **candidates** for reduction, never proof that a log is safe to drop. Critical audit/security/incident events require owner approval.
- Byte totals are estimates based on selected raw line lengths. They are not Loki billable storage or compression measurements.
- A zero-anomaly result does not establish system health; missing logs and retention cannot be diagnosed from a local file.

## Next stages (not implemented)

| Version | Scope |
|---|---|
| v0.2 | Read-only Loki adapter with bounded time windows, auth, validation and incomplete-export reporting |
| v0.3 | Scheduled baselines and before/after comparisons; optional Kubernetes workload discovery |
| v0.4 | Approved LLM review, developer Cursor pack, optional MCP integration, policy-based quality scoring |

Reference learning sample: [CloudDevOpsHub/AIOPS](https://github.com/CloudDevOpsHub/AIOPS). The SmartLog implementation is independent and does not copy that repository's Python scripts.
