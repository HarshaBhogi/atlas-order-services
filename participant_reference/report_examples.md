# Sample Assessment Reports

These are fictional examples. Names, services, identifiers, and evidence excerpts are invented.

## Confirmed finding

| Field | Example |
| --- | --- |
| Identifier | RPT-104 |
| Title | Record export did not apply the tenant predicate |
| Scope | `billing/export_service.py`, change set `4a2f` |
| Classification | CWE-862, OWASP A01:2025 |
| Severity / confidence | High / High |
| Evidence | A new export query accepts a record identifier but the service does not call the existing tenant policy helper used by adjacent operations. A test using two fictitious tenants returns the second tenant's record. |
| Impact | An authenticated caller could receive records assigned to a different tenant. |
| Recommended change | Reuse the established policy helper before fetching the export record and add a cross-tenant regression test. |
| Verification | The test should receive a denial or a not-found result for the other tenant. |
| Follow-up | Confirm whether a privileged support role is intentionally exempt from the tenant policy. |

## Confirmed finding with a dependency record

| Field | Example |
| --- | --- |
| Identifier | RPT-117 |
| Title | Production image retained a component with a published advisory |
| Scope | `container/requirements.lock` |
| Classification | Software supply chain review; see the CVE record cited by the dependency scanner. |
| Severity / confidence | Medium / Medium |
| Evidence | The lock file resolves `sample-parser` to a version named in a scanner result. The container build installs the lock file. |
| Impact | The deployment image retains the affected component until the version is changed or the component is removed. |
| Recommended change | Upgrade to an advisory-fixed release, regenerate the lock file, and verify the resulting image inventory. |
| Verification | Rebuild the image and rerun the dependency inventory and test suite. |
| Follow-up | Confirm that the identified component is part of the deployed execution path. |

## Non-actionable observation

| Field | Example |
| --- | --- |
| Identifier | OBS-031 |
| Title | Query builder accepted only fixed ordering choices |
| Scope | `catalog/query_builder.py` |
| Classification | No reportable issue |
| Severity / confidence | Informational / High |
| Evidence | User input is passed through a named query parameter. The sort option maps to a fixed set of column expressions before a statement is created. |
| Decision | Do not report as a finding. Keep the current test coverage for unsupported sort values. |

## Report-writing checklist

- Separate observed facts from inferred impact.
- Cite the exact reviewed revision, file, symbol, or request sequence.
- Include the rule or policy basis for the classification.
- Explain why the conclusion is in scope for the reviewed change.
- Give an outcome-oriented verification step.
- Mark operational assumptions and ownership questions for confirmation.
