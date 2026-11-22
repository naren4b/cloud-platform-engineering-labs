# SmartLog: Log Quality Analyzer

**Status:** v0.2 preview, offline noise-review guidance with synthetic tests.

SmartLog is a lightweight Python log-analysis lab. It helps developers find frequent log patterns, identify ERROR bursts, measure severity and approximate log bytes, and create review packs for source-code improvements. **It does not automatically decide which logs to delete.**

## Architecture

See [the scalable architecture](docs/ARCHITECTURE.md) and [next-action prompts](docs/NEXT-ACTIONS.md). The current application is local, not an enterprise multi-tenant service.


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

Run this from the `ai-engineering/smartlog` directory:

~~~bash
docker run --rm -v "$PWD:/app" -w /app -e PYTHONDONTWRITEBYTECODE=1 --entrypoint python smartlog:local -m unittest discover -s tests -v
~~~

The tests cover parsers, diagnostics, synthetic fixtures under `tests/fixtures/`, and the Streamlit empty states (via `streamlit.testing`). All fixtures are synthetic. Do not add production logs to the repository.

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

## Features

- Paste or upload .txt, .log, or .jsonl, or use bundled synthetic logs.
- Pluggable parsers in `parsers.py`. Each parser is a `LineParser` subclass, so new formats do not change the analysis engine.
- Auto-detect or manually select a format in the **Log format** selector: `auto`, `jsonl`, `logfmt`, `kubernetes-cri`, or `text`.
- Parse ISO timestamp-first logs with optional severity and brackets, common Kubernetes CRI log lines, JSONL (including Docker log envelopes), and logfmt/logrus records (`time=… level=… msg=…`). Parse Unix epoch timestamps in structured logs.
- Attach multiline records: whitespace-led lines, `Caused by:`, `... N more`, and lines starting with `}`, `]` or `"` are counted as continuation lines and attached to the preceding line. They are never discarded.
- Application-specific formats through an optional rules JSON (upload in the **Custom parser rules** expander). Rules are regex-based with a named timestamp, level, and message. Keep real rules files local and out of git. `tests/fixtures/app_rules.json` shows the format.
- Mark records without an explicit severity as UNKNOWN, rather than guessing their severity.
- Show safe parsing diagnostics without exposing unparsed raw lines: total input, blank, parsed, skipped by time range, unsupported, malformed, continuation, detected format, and parse success %. Success % is `(parsed + skipped + continuation) / (non-blank lines)`.
- Handle zero parsed records and empty result sets without crashing the dashboard. Shows "No matching log format detected." and renders no charts. Use the parser selector or a rules file for unsupported formats.
- Filter logs by UTC date; timestamps without a timezone are interpreted as UTC.
- Show severity counts, top normalized message templates, approximate bytes, and fixed 30-second ERROR bursts.
- Rank explainable noise candidates and protect likely audit, security and critical events; never treat frequency as proof that logging is safe to suppress.
- Produce a next-action developer prompt without log messages or source identifiers. Aggregate counts may still be confidential.
- Download Markdown, JSON, CSV and next-action prompts for approved local review.
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
| v0.2 (preview) | Offline noise-review candidates and safe follow-up prompts |
| v0.3 | Read-only Loki adapter with bounded time windows, auth and completeness reporting |
| v0.4 | Scheduled baselines, before/after comparisons and optional Kubernetes discovery |
| v0.5 | Optional approved LLM, Cursor/MCP integrations and detailed policy scoring |

Reference learning sample: [CloudDevOpsHub/AIOPS](https://github.com/CloudDevOpsHub/AIOPS). The SmartLog implementation is independent and does not copy that repository's Python scripts.
