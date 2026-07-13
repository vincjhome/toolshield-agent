# Project Plan

## Project Scope

### What This Project Demonstrates

ToolShield Agent demonstrates a three-tier approach to AI security classification:
a base LLM, a fine-tuned version of that model, and a fine-tuned model augmented with
retrieval-augmented generation (RAG). All three tiers are evaluated on the same fixed
set of agentic tool-call security scenarios so that performance differences are directly attributable
to the addition of fine-tuning and RAG respectively.

The core claim under test: a domain-adapted model with access to grounded security policy
produces more accurate, more consistent, and more actionable threat classifications than
a general-purpose base model.

---

### What Fine-Tuning Is Expected to Add

- **Consistent output structure** — base models may free-form their answers; fine-tuning enforces the
  seven-field analyst format (Classification, Attack Type, Tool Boundary Violated, Risk Reason,
  Potential Impact, Recommended Control, Confidence) reliably.
- **Attack taxonomy fluency** — the model learns to distinguish closely related attack types
  (e.g., `direct_prompt_injection` vs. `indirect_prompt_injection`, `privilege_escalation` vs.
  `unauthorized_tool_invocation`) from labeled examples.
- **Tool boundary awareness** — the model learns which tool categories carry elevated risk and
  should apply higher scrutiny thresholds.
- **Reduced false negatives** — exposure to labeled malicious sequences makes the model less likely
  to classify dangerous sequences as safe due to surface-level plausibility.

---

### What RAG Is Expected to Add

- **Policy grounding** — retrieval from `agent_tool_security_policy.md` anchors recommendations
  to explicit, auditable rules rather than model priors.
- **Standards alignment** — retrieval from OWASP LLM Top 10 notes ensures that attack type labels
  and recommended controls align with industry-recognized frameworks.
- **Reduced hallucination in recommendations** — the model cites retrieved policy text rather than
  generating plausible-sounding but unverifiable controls.
- **Extensibility** — new threat categories can be added to the RAG corpus without retraining,
  allowing the knowledge base to be updated independently of the model weights.

---

### What Is Intentionally Out of Scope

Given the prototype scope of this project, the following are explicitly excluded:

- **Full dataset scale** — the training set will contain a small representative set of examples
  per attack type, not a production-scale corpus.
- **Automated evaluation metrics** — scoring is qualitative (human review of the three test
  question outputs) rather than automated precision/recall benchmarks.
- **Real-world fine-tuning infrastructure** — fine-tuning uses available API or notebook tooling;
  no custom distributed training setup.
- **Multi-turn agentic simulation** — all tool-call sequences are single-session snapshots,
  not live multi-step agent traces.
- **Red-teaming beyond the three test questions** — adversarial stress testing beyond the defined
  evaluation set is out of scope.
- **Deployment or serving** — no API endpoint, no production inference pipeline.

---

## Phases

| Phase | Tasks | Status |
| --- | --- | --- |
| 1 | Folder setup, schema definition, project plan | Complete |
| 2 | Training dataset construction (`training_data.jsonl`) | Pending |
| 3 | Fine-tuning run and base model baseline capture | Pending |
| 4 | RAG pipeline setup (chunking, embedding, retrieval) | Pending |
| 5 | Three-tier evaluation on test questions | Pending |
| 6 | Output documentation, screenshots, reflection | Pending |
