# Agent Memory

**ID:** AI-07  
**Priority:** P2  
**Status:** Deferred  
**Learning target:** December 2026 or later

## Overview

Explore persistent investigation notes without accumulating unsafe or stale context.

## Technical Scope

- Separate temporary conversation context from durable incident notes.
- Add expiration, source tracking and deletion controls.
- Test retrieval of a prior synthetic incident.

## Design Considerations

- **Data:** Start with synthetic logs; do not copy employer or customer data to personal tools.
- **Safety:** Keep tools read-only and validate input/output boundaries.
- **Cost:** Prefer a local demo. Estimate API or cloud spend before enabling it.
- **Approach:** Implement the smallest testable version before adding framework features.

## Acceptance Criteria

- [ ] Reuse relevant prior findings without asserting they are current facts.
- [ ] Delete an incident note and verify it is no longer returned.
- [ ] Avoid saving credentials or personal/corporate sensitive data.

## Links

- [AI Engineering Lab Index](../README.md)
- [December Learning Plan](https://github.com/naren4b/my-ai-hub/blob/main/my-ai/my-learning/2026-12-ai-python-projects.md) (pending merge in my-ai-hub)
