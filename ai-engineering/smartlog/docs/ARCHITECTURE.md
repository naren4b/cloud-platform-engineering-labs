# SmartLog: Enterprise-Scale Solution Architecture

**Status: target design, not yet implemented.** The current Streamlit app is a bounded
local demo. It must not be deployed unchanged as a cluster-wide logging service.

## Goal

Provide a source-independent, format-extensible logging-quality auditor for
any organization. It finds low-value logging candidates and recommends
next actions, without changing the primary ingestion path or deleting logs.

A universal parser cannot guarantee understanding of every unknown format.
Unknown formats must be measurable as parsing gaps. Plug-in parsers extend
support without rewriting the core analyzer.

## Architecture

~~~mermaid
flowchart TD
  File[Paste / file / object storage] --> Source[Source adapters]
  Loki[Loki / OpenSearch / cloud APIs] --> Source
  K8s[Bounded Kubernetes pod reads] --> Source
  OTLP[Optional OTLP events] --> Source
  Source --> Jobs[Job admission / time windows / checkpoints]
  Jobs --> Workers[Bounded worker pool]
  Workers --> Schema[OpenTelemetry-inspired LogRecord]
  Schema --> Rules[Pattern statistics + protected-log policies]
  Rules --> Results[Findings / evidence / uncertainty]
  Results --> UI[Reports + dashboard]
  Results --> Prompt[Next-action prompts]
  Auth[Auth, tenant quotas, secrets and egress control] -.-> Source
  Auth -.-> Jobs
  Auth -.-> UI
~~~

## Canonical normalized record

Use the OpenTelemetry Logs Data Model as a guide:
timestamp, observed timestamp, severity text and number, body,
attributes, resource, optional trace/span IDs. Add:
- organization/tenant ID and source ID;
- parser name/version, parse status and original byte length;
- an opaque tenant-scoped pattern fingerprint;
- source-window completeness and sample/approximation metadata.

Preserve unknown severity and parsing failures. Raw content belongs in the
approved execution boundary, not in public reports or unapproved LLM prompts.

## Connectors

Each connector should implement bounded discovery, read-window, checkpoint,
source statistics and close methods. Add adapters for uploaded files, Loki,
OpenSearch, approved cloud logging APIs, object storage and approved event streams.

- Loki: read-only LogQL, scoped label selectors, bounded query_range windows,
  per-tenant query limits, backoff and checkpointing. Avoid high-cardinality
  cluster-wide queries. Detect backend result limits and equal-timestamp ties.
  Mark truncated or uncertain windows as incomplete, not complete.
- Kubernetes: pod log retrieval only for bounded debugging, never scrape all
  pods as the primary log archive. Kubernetes Service URLs are not log sources.
- Ingestion adapters may consume OTLP via an authorized gateway, but SmartLog
  must not sit between applications, Grafana Alloy and Loki.
- Source URLs are allowlisted. Block SSRF and internal-network discovery.
  Use tenant-scoped secrets and read-only credentials.

## Scale levels

Local: one Docker container, in-memory state, 5 MiB limit.

Team: independent API/UI service and background workers, persistent job
checkpoints, scoped source queries and time-window budgets.

Enterprise: tenant-isolated jobs, scheduler, durable queue, horizontally
scaled workers, encrypted report storage, quotas and per-source rate limits.

For busy Kubernetes clusters:
- Separate API/UI pods from CPU-heavy analysis workers.
- Limit concurrency per tenant, service, time window and backend.
- Process chunks in bounded memory. Use capped top-K algorithms where needed,
  and declare when results are approximate or sampled.
- Maintain durable checkpoints, retry budgets, cancellation and backpressure.
- Scale worker replicas using queue lag and CPU, not raw cluster log volume.
- Set CPU/memory requests and limits, readiness probes, disruption policies,
  ingress authentication, network policies and egress restrictions.
- Prefer scheduled baseline queries and source-side aggregates to continuous
  full-stream copying. Never overload Loki or the Kubernetes API.
- Expose audit job metrics: throughput, latency, errors, completeness,
  queue age, truncation, rejected requests and precision of recommendations.
- Under overload, defer or fail audits visibly. Do not affect application
  logging or claim missing logs are absent anomalies.

## Noise-quality policy

- Count events, bytes, repeated templates, periodicity, bursts and context.
- Separate noise candidates from protected and unknown events.
- Never equate high frequency with a log that is safe to delete.
- Recommendations: KEEP, REVIEW_REDUCE, REVIEW_DEBUG, REVIEW_METRIC,
  INVESTIGATE or PROTECTED. All require review by the service owner.
- Compare before/after volume under similar load and preserve incident,
  security and compliance evidence before considering any production change.
- Initial v0.2 heuristics use only frequency and byte share. They do not
  measure diagnostic usefulness or provide validated cost savings.

## Data protection and portability

Use only synthetic fixtures in this public repository. Corporate data,
source-specific rules, identifiers and proprietary code remain in approved
corporate systems. No automatic copying between environments.
A privacy-minimized prompt contains no raw templates or source names, but
even aggregate numbers might require corporate approval before sharing.
LLMs are strictly optional and never part of the hot ingestion path.

## Delivery steps

1. v0.2: Offline noise candidates + deterministic next-action guidance.
2. v0.3: Source adapter contract + bounded read-only Loki pilot.
3. v0.4: Job scheduler, checkpoints, tenant quotas, load testing.
4. v0.5: Approved local reasoning, MCP, and source-code review integrations.

Before rollout, set explicit throughput, CPU, memory, source-query and
safety acceptance targets based on actual authorized load tests.

## References

- OpenTelemetry Logs Data Model: https://opentelemetry.io/docs/specs/otel/logs/data-model/
- Grafana Loki API: https://grafana.com/docs/loki/latest/reference/loki-http-api/
- OpenTelemetry Collector scaling: https://opentelemetry.io/docs/collector/scaling/
- Kubernetes HPA: https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
