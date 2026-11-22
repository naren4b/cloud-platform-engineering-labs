# GraphRAG

**ID:** AI-03  
**Priority:** P2  
**Status:** Deferred  
**Learning target:** December 2026 or later

## Overview

Explore whether a service dependency graph helps explain cross-service incidents better than plain search.

## Technical Scope

- Create a small service-to-service dependency graph from synthetic data.
- Attach incident events and change records to graph nodes.
- Retrieve relevant graph neighbors with supporting log evidence.

## Design Considerations

- **Data:** Start with synthetic logs; do not copy employer or customer data to personal tools.
- **Safety:** Keep tools read-only and validate input/output boundaries.
- **Cost:** Prefer a local demo. Estimate API or cloud spend before enabling it.
- **Approach:** Implement the smallest testable version before adding framework features.

## Acceptance Criteria

- [ ] Trace a simulated incident through two dependent services.
- [ ] Explain the origin of every graph relationship.
- [ ] Compare against baseline search before claiming improvement.

## Links

- [AI Engineering Lab Index](../README.md)
- [December Learning Plan](https://github.com/naren4b/my-ai-hub/blob/main/my-ai/my-learning/2026-12-ai-python-projects.md) (pending merge in my-ai-hub)
