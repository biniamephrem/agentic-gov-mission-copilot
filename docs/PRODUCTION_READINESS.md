# POC-to-Production Readiness Checklist

## Discovery
- Define mission outcome and measurable user task.
- Identify authoritative data sources and classification boundaries.
- Define actions the AI may recommend versus execute.
- Identify accountable human decision authority.

## Architecture
- Select approved model endpoint and region.
- Select vector/search store with document ACL filtering.
- Define identity, role, and attribute authorization model.
- Separate model, retrieval, and tool execution identities.

## Security
- Complete threat model for prompt injection, exfiltration, and tool abuse.
- Enforce private networking and egress restrictions.
- Encrypt state, evidence, prompts, outputs, and audit data.
- Send logs to approved SIEM.

## Reliability
- Define SLOs for availability and mission latency.
- Add retries, timeouts, circuit breakers, and fallback models.
- Add failure-safe behavior: when uncertain, stop rather than execute.

## Evaluation
- Build golden mission-task data with SMEs.
- Add adversarial and prompt-injection test cases.
- Establish pre-deployment quality/safety thresholds.
- Re-run evaluations on every model, prompt, retrieval, or tool change.

## Operations
- Implement model/prompt/version tracking.
- Establish incident response and rollback.
- Review human-approval rates and false-positive/negative patterns.
- Continuously curate mission data and feedback.
