# Context Assembler

**ID:** AI-01  
**Priority:** P1  
**Status:** Planned  
**Learning target:** December 2026

## Overview

Build a small context builder that selects relevant log samples, request IDs, timestamps and runbook snippets for one question.

## Technical Scope

- Define a schema for log events and supporting context.
- Rank and truncate context within a token budget.
- Record exactly which evidence was provided to the model.

## Design Considerations

- **Data:** Start with synthetic logs; do not copy employer or customer data to personal tools.
- **Safety:** Keep tools read-only and validate input/output boundaries.
- **Cost:** Prefer a local demo. Estimate API or cloud spend before enabling it.
- **Approach:** Implement the smallest testable version before adding framework features.

## Acceptance Criteria

- [ ] Given noisy synthetic logs, retain events relevant to an incident.
- [ ] Enforce a fixed context budget and show what was excluded.
- [ ] Show source IDs for every returned evidence item.

## Links

- [AI Engineering Lab Index](../README.md)
- [December Learning Plan](https://github.com/naren4b/my-ai-hub/blob/main/my-ai/my-learning/2026-12-ai-python-projects.md) (pending merge in my-ai-hub)
