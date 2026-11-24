# Assessment Worksheet

Use one worksheet per reportable item. Keep supporting artifacts with the assessment submission rather than altering the reviewed code.

```text
Assessment ID:
Reviewed revision or patch:
Reviewer:
Date:

1. Scope
   - Changed files and lines:
   - Relevant unchanged context:
   - External assumptions:

2. Observation
   - What behavior or construction was observed?
   - What input, identity, configuration, or deployment condition matters?

3. Classification
   - Category and standard mapping:
   - Severity:
   - Confidence:
   - Disposition: true_positive | false_positive | needs_context | non_actionable

4. Evidence
   - File, symbol, and line or patch hunk:
   - Request or test sequence:
   - Expected versus observed result:

5. Impact and recommendation
   - Affected asset or boundary:
   - Proposed engineering outcome:
   - Verification step:
   - Engineer confirmation needed:
```

## Review sequence

1. Begin with changed lines for the stated task.
2. Follow dependencies into only the surrounding code necessary to understand behavior.
3. Separate newly introduced behavior from conditions that predate the change.
4. Test or otherwise verify at least one proposed correction.
5. Record uncertainty explicitly rather than overstating confidence.
