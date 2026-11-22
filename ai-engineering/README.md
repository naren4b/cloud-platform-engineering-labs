# AI Engineering Labs

These 12 ideas are captured for **December 2026** as a learning backlog.
They are not 12 committed deployments. The first implementation is [SmartLog](smartlog/README.md), a local logging-quality analyzer. Other project ideas remain a December learning backlog.

Source: [LinkedIn list of 12 advanced AI engineering project ideas](https://lnkd.in/p/gu4RWnmb).

## Project catalog

| ID | Project | Priority | Suggested implementation | Status |
| --- | --- | --- | --- | --- |
| AI-01 | Context Assembler | P1 | Select relevant logs and metadata for AI analysis | Planned |
| AI-02 | Hybrid Retrieval | P1 | Combine exact log filters with semantic search | Planned |
| AI-03 | GraphRAG | P2 | Explore service and incident relationships | Deferred |
| AI-04 | Self-Correcting Agentic RAG | P0 | Validate log evidence and retry weak retrieval | Planned |
| AI-05 | Durable Agent State Machine | P0 | Resume interrupted audits without losing checkpoints | Planned |
| AI-06 | Custom MCP Tool Server | P0 | Expose approved, read-only Loki queries | Planned |
| AI-07 | Agent Memory | P2 | Persist investigation context safely | Deferred |
| AI-08 | Multi-Agent System | P2 | Compare separate roles against a simpler single agent | Deferred |
| AI-09 | Agent Evaluation Pipeline | P0 | Measure accuracy, false positives and repeatability | Planned |
| AI-10 | Agent Security Gateway | P0 | Enforce tool permissions and data boundaries | Planned |
| AI-11 | Semantic Cache | P1 | Skip repeated analysis of unchanged log patterns | Planned |
| AI-12 | AI Architecture Deep Dive | P0 | Record design, reliability, cost and security trade-offs | Planned |

P0 = December core; P1 = stretch; P2 = later.

## December plan

- **Week 1, Dec 1-6:** Extend SmartLog log parsing and baseline quality checks; explore read-only MCP (#6)
- **Week 2, Dec 7-13:** Evidence retrieval and self-correction (#4), context assembly (#1)
- **Week 3, Dec 14-20:** Durable state (#5), evaluation (#9), security gateway (#10)
- **Week 4, Dec 21-27:** Architecture review (#12), optional hybrid retrieval (#2) and caching (#11)
- **Dec 28-31:** Review results and reprioritize incomplete work

## Implementation plan

First lab: [SmartLog](smartlog/README.md) in `ai-engineering/smartlog/` (v0.1 MVP). Build locally using synthetic logs before any approved corporate integration.

The solution should use synthetic logs locally at first. Corporate data and
Loki integration require approval and must stay in approved corporate systems.
Use read-only queries. No automatic deletion or production configuration changes.

Use free, open-source learning tools where practical. Estimate and approve any
cloud/API costs before provisioning. Cursor can help with small implementation
steps and test generation, but outputs require review.

## Ownership and navigation

- **This repository:** engineering catalog and future runnable labs
- **[December learning roadmap](https://github.com/naren4b/my-ai-hub/pull/109):** schedule, priorities and learning checkpoints (review PR, not yet merged)
- **[AI platform portfolio](https://github.com/naren4b/my-ai-platform):** architectural case studies and evidence links only
- Do not duplicate implementation code across repositories

## Definition of done for the first lab

- Reproducible local demo with test data
- Baseline log-noise metrics and evaluated quality findings
- Secure read-only tool access with failure handling
- A minimal architecture diagram and a cost/security note
- No claims of production impact without measured evidence
