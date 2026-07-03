# CIB-8 Lessons Learned

## Purpose

Track operational lessons so CIB-8 improves without unsafe autonomy.

## Lesson Format

```text
Date:
Case ID:
What happened:
What worked:
What failed:
Evidence quality lesson:
Agent coordination lesson:
Prompt/tooling change recommended:
Approved by human operator: Yes / No
```

## Seed Lesson

```text
Date: bootstrap
Case ID: seed-001
What happened: CIB-8 was defined as an orchestrator, not a single investigator.
What worked: Separating the eight layers clarified deployment and control.
What failed: Over-focusing on inspirational repos temporarily obscured the original 8-layer requirement.
Evidence quality lesson: Architecture must preserve claim -> evidence -> source -> confidence.
Agent coordination lesson: The Orchestrator controls agents; agents do not self-deploy without mission scope.
Prompt/tooling change recommended: Add CIB-8 folder and role files before deeper code integration.
Approved by human operator: Pending
```
