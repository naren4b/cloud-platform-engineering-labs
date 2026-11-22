# Next-Action Prompt Contract

SmartLog should not end with charts. Every analysis should suggest a concrete
safe next action based on evidence, coverage and potential operational risk.

| Evidence | First suggested action |
| --- | --- |
| Zero parsed events | Diagnose format locally, write synthetic fixture, add parser |
| High repeated INFO/DEBUG volume | Review logging callsite, aggregation, frequency, metric |
| Repeated WARN | Investigate retry loop or repeated failure |
| ERROR/CRITICAL/security/audit events | Preserve and investigate; never blindly filter |
| Unknown severity | Repair structured logging or severity field |
| No clear candidate | Compare longer, representative baseline windows |
| Partial source coverage | Repair query limits or parser coverage before ranking |

Each generated prompt should ask for:
1. Evidence and assumptions, including coverage and sampling.
2. Potential diagnostic and compliance loss.
3. Smallest safe change for service-owner review.
4. Synthetic regression tests.
5. Comparable before/after validation.
6. No automatic changes to production.

The default prompt must exclude message templates, raw log bodies, service
names, internal endpoints and credentials. Operational counts can still be
confidential, so all prompts remain local until approved for sharing.

## Example of expected developer direction

~~~text
Act as a Principal SRE in this approved corporate environment.
Review the highest-volume INFO pattern using only the local detailed report.
Find the logging callsite in the approved repository.
Recommend KEEP, REDUCE, DEBUG, METRIC or INVESTIGATE.
Explain evidence, confidence and risks of lost diagnostic context.
Preserve audit, security and critical failure logs.
Propose a minimal patch for human review and a synthetic test.
Estimate potential savings separately from measured savings.
Do not change production configuration automatically.
Do not upload raw logs or source code to external systems.
~~~
