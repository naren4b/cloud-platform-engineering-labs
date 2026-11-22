# SmartLog: Log Quality Analyzer

**Status:** v0.1.1 MVP, offline synthetic-data demo (parser and empty-state fix).

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

## Run locally with Docker (default)

**Host prerequisite: Docker only.** Do not install Python, pip, venv, or Streamlit on the host.

From the repository root, build once (and rebuild after pulling source updates):

~~~bash
docker build -t smartlog:local ai-engineering/smartlog
~~~

Run the complete application:

~~~bash
docker run --rm --name smartlog -p 127.0.0.1:8501:8501 smartlog:local
~~~

Open http://localhost:8501 and select **Synthetic demo**. Stop the container with Ctrl+C. To run the unit tests inside Docker:

~~~bash
docker run --rm --entrypoint python smartlog:local -m unittest discover -s tests -v
~~~

### Prebuilt image, no local build (after publication)

The GitHub Actions workflow builds and publishes `ghcr.io/naren4b/smartlog:latest` to GitHub Container Registry when merged to `main`. Once the package is published and made accessible to your account (public visibility or an approved login), you can run it directly:

~~~bash
docker run --rm --name smartlog -p 127.0.0.1:8501:8501 ghcr.io/naren4b/smartlog:latest
~~~

This image is **not available until the workflow has completed successfully and package visibility is configured**. For repeatable work, prefer an immutable version or digest over `latest`.

### Optional: inspect or test inside a container

Python and dependencies are available inside the image:

~~~bash
docker run --rm -it --entrypoint sh smartlog:local
~~~

No host Python setup is required for development, testing, or running SmartLog.

## v0.1 features

- Paste or upload .txt, .log, or .jsonl, or use bundled synthetic logs.
- Parse ISO timestamp-first logs with optional severity and brackets, common Kubernetes CRI log lines, and JSONL (including Docker log envelopes). Parse Unix epoch timestamps in structured logs.
- Mark records without an explicit severity as UNKNOWN, rather than guessing their severity.
- Show safe parsing failure categories and success percentage without exposing unparsed raw lines.
- Handle zero parsed records and empty result sets without crashing the dashboard. Unsupported formats still need a custom parser.
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
