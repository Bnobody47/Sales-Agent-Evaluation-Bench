# Audit Memo (Act I)

Public benchmarks such as tau2-bench retail grade generic completion quality, but they do not grade Tenacious-specific sales safety. Week 10 evidence shows this gap is structural: the agent can be fluent while still making commercially invalid commitments.

**Gap 1: Bench over-commitment (non-obvious, operational failure).**  
In probes `P-007`, `P-008`, and `P-009`, the model commits staffing before validating bench feasibility. The same pattern appears in traces `tau_dev_tier_baseline_01` and `tau_dev_tier_baseline_02` where optimistic commitment language is produced despite low-support conditions. This is not a wording defect; it is a policy and delivery-truth defect. A public benchmark can score such outputs as “helpful” while Tenacious would treat them as trust-breaking.

**Gap 2: Grounding failures under weak public signal.**  
Probes `P-004`, `P-005`, `P-006`, `P-028`, `P-029`, and `P-030` show unsupported assertions when evidence is sparse. In trace `tau_reproduction_check_02`, the model still generates assertive framing after inconsistent signal context. Public benchmarks often reward plausibility; Tenacious requires claim-to-signal grounding. If the signal is weak, the correct action is question-first phrasing or abstention.

**Gap 3: Style-guide drift under objection pressure.**  
Probes `P-010`, `P-011`, and `P-012` show that outputs degrade from Tenacious style markers (direct, grounded, honest, professional, non-condescending) in multi-turn pressure. Trace `tau_reproduction_check_03` reflects this instability pattern in a reproduction run where form remains fluent but trust-preserving tone constraints are not consistently met. Generic benchmarks do not evaluate Tenacious marker-level style fidelity.

**Gap 4: Dual-control and workflow-state coordination failures.**  
Probes `P-019`, `P-020`, `P-021`, `P-022`, `P-023`, and `P-024` demonstrate errors in decision sequencing: pushing scheduling when clarification is needed, or mishandling channel/timezone state. In trace `tau_reproduction_check_04`, the process pattern is “action-first” despite control-state ambiguity. Single-turn public tasks rarely model these state transitions, so these failures are undercounted.

**Gap 5: Cross-thread integrity and consent/state leakage.**  
Probes `P-013`, `P-014`, and `P-015` capture context leakage across threads/channels. This appears as a reliability and compliance risk pattern aligned with trace `tau_reproduction_check_05` behavior where context carryover assumptions are brittle. Public benchmarks usually do not include thread-isolation checks.

These gaps are distinct: (1) commitment truthfulness, (2) evidence grounding, (3) brand-style preservation, (4) workflow control-state correctness, and (5) thread isolation integrity. At least one is non-obvious and mechanism-level (bench over-commitment). Therefore, Tenacious-Bench v0.1 must score policy-safe commitments, evidence-linked claims, marker-level tone adherence, and process-state correctness with mechanical checks plus calibrated judge scoring.
