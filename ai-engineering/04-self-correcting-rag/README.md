# Self-Correcting Agentic RAG

**ID:** AI-04  
**Priority:** P0  
**Status:** Planned  
**Learning target:** December 2026

## Overview

Build an evidence-grounded log investigation that detects weak retrieval and performs a bounded retry.

## Technical Scope

- Retrieve log evidence for a question and draft a finding.
- Check whether cited sources support the finding.
- Retry once using a revised query and stop on insufficient evidence.

## Design Considerations

- **Data:** Start with synthetic logs; do not copy employer or customer data to personal tools.
- **Safety:** Keep tools read-only and validate input/output boundaries.
- **Cost:** Prefer a local demo. Estimate API or cloud spend before enabling it.
- **Approach:** Implement the smallest testable version before adding framework features.

## Acceptance Criteria

- [ ] Reject a plausible but unsupported finding.
- [ ] Prevent unbounded loops and return a clear uncertain result.
- [ ] Record the evidence and retry path for reproducibility.

## Links

- [AI Engineering Lab Index](../README.md)
- [December Learning Plan](https://github.com/naren4b/my-ai-hub/blob/main/my-ai/my-learning/2026-12-ai-python-projects.md) (pending merge in my-ai-hub)
