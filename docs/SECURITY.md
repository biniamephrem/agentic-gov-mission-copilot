# Security and Authorization Model

This public repository demonstrates security design patterns; it is not an Authority to Operate (ATO) package.

## Core controls

1. **Human authorization boundary** — high-impact tools cannot execute directly from model output.
2. **Tool allow-list** — only explicitly registered tools can be called.
3. **Typed tool arguments** — production implementations should enforce JSON Schema/Pydantic validation per tool.
4. **Least privilege** — retrieval, model invocation, and tool execution should run under separate service identities.
5. **Evidence controls** — production RAG must enforce source-level access controls and classification boundaries.
6. **Auditability** — mission request, retrieval sources, approval decision, and tool execution are separately logged.
7. **Private networking** — use VPC endpoints/private endpoints and deny public service access when supported.
8. **Encryption** — KMS/CMK-backed encryption for data at rest and TLS for data in transit.
9. **Secrets** — store provider credentials in Secrets Manager/Key Vault, never source control.
10. **Model safety** — include prompt injection tests, tool misuse tests, data exfiltration tests, and context-boundary tests.

## Production hardening

- Integrate workforce identity (CAC/PIV, agency SSO) and ABAC/RBAC.
- Map tool authorization to user identity, mission role, and environment.
- Require dual authorization for selected mission actions.
- Add content/data labeling and source ACL filtering in retrieval.
- Add tamper-resistant audit storage and SIEM forwarding.
- Add rate limits, circuit breakers, timeouts, and model fallback strategy.
- Establish model/version change control and rollback procedures.
- Run continuous evaluations before promotion to production.
