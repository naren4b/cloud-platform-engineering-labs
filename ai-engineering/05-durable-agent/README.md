# Durable Agent State Machine

**ID:** AI-05  
**Priority:** P0  
**Status:** Planned  
**Learning target:** December 2026

## Overview

Make a log audit resumable after process crashes or timeouts.

## Technical Scope

- Model states for collect, analyze, validate and report.
- Persist checkpoints without storing secrets or raw sensitive logs.
- Make retries idempotent and handle partial failures.

## Design Considerations

- **Data:** Start with synthetic logs; do not copy employer or customer data to personal tools.
- **Safety:** Keep tools read-only and validate input/output boundaries.
- **Cost:** Prefer a local demo. Estimate API or cloud spend before enabling it.
- **Approach:** Implement the smallest testable version before adding framework features.

## Acceptance Criteria

- [ ] Interrupt an audit and resume it from the last safe checkpoint.
- [ ] Show that retries do not create duplicate reports.
- [ ] Test timeout and corrupt-checkpoint recovery.

## Links

- [AI Engineering Lab Index](../README.md)
- [December Learning Plan](https://github.com/naren4b/my-ai-hub/blob/main/my-ai/my-learning/2026-12-ai-python-projects.md) (pending merge in my-ai-hub)
