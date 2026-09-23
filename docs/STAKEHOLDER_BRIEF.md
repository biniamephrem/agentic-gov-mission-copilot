# Mission Stakeholder Brief

## What this system does

The Mission Copilot helps an authorized analyst review mission reports, identify relevant evidence, summarize the situation, and prepare a proposed operational action.

## What it does not do

The model is not given independent authority to execute high-impact operational actions. When the workflow proposes an action such as allocating a scarce mission resource, execution stops until an authorized human approves or rejects the proposal.

## Why this matters

This design separates **AI assistance** from **human decision authority**. The AI can reduce time spent finding and synthesizing information while preserving a clear approval boundary for consequential actions.

## What operators can inspect

Operators can review:

- Which mission records were retrieved.
- The AI-generated assessment.
- The exact proposed tool call and arguments.
- The risk classification that triggered approval.
- Who approved or rejected the action.
- The result returned by the downstream system.

This creates a traceable record for mission review, troubleshooting, security monitoring, and continuous improvement.
