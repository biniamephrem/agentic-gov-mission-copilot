# Evaluation Strategy

High-stakes agentic systems need more than generic answer-quality testing.

## Evaluation dimensions

| Dimension | Example metric |
|---|---|
| Retrieval | Evidence source recall@k |
| Grounding | Supported-claim rate |
| Tool correctness | Valid tool/schema selection rate |
| Human authorization | % of high-impact actions blocked pending approval |
| Safety | Prompt-injection/tool-abuse success rate |
| Reliability | Task completion rate and retry/fallback rate |
| Latency | P50/P95 end-to-end time |
| Cost | Cost per completed mission task |
| Drift | Weekly change in task and safety metrics |

## Promotion gate example

A model/workflow revision should not deploy when:

- Any high-impact action bypasses human authorization.
- Grounded factual accuracy falls below the program threshold.
- Tool schema validity regresses.
- Prompt-injection resistance regresses on the approved red-team suite.
- Critical operational latency exceeds the mission SLO.
