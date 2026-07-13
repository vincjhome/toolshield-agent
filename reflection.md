# Project Reflection — ToolShield Agent

## Project Summary

ToolShield Agent is a domain-specialized security AI for classifying AI agent tool-call sequences as safe, suspicious, or malicious. It was built across three tiers to demonstrate how fine-tuning and retrieval-augmented generation each add distinct value over a general-purpose base model.

| Tier | Model | Configuration |
| --- | --- | --- |
| Base | `unsloth/Llama-3.2-3B-Instruct` | No adaptation |
| Fine-tuned | LoRA-adapted from base | Trained on 120 synthetic security examples |
| Fine-tuned + RAG | Fine-tuned model via Ollama | LangFlow + ChromaDB retrieval over ToolShield policy source document |

---

## 1. What Does Fine-Tuning Add Over a Base Model?

The base model was able to recognize some risky behavior in agent tool-call sequences — it had enough general knowledge to flag things like access to `/etc/passwd` or bulk email sends as potential concerns. However, its classifications were less consistent. In several cases, clearly malicious examples — such as a jailbreak leading directly to a sensitive file read, or an unsigned system message triggering an admin grant — were labeled as only suspicious rather than malicious. The base model also did not reliably produce the seven-field structured output format required for ToolShield analyst responses.

Fine-tuning on the 120-example synthetic dataset changed both of these things. The fine-tuned model learned the structured ToolShield response format — Classification, Attack Type, Tool Boundary Violated, Risk Reason, Potential Impact, Recommended Control, Confidence — and applied it consistently across evaluation inputs. It also learned the security taxonomy specific to agentic systems: distinguishing `indirect_prompt_injection` from `direct_prompt_injection`, recognizing `excessive_agency` as distinct from `unauthorized_tool_invocation`, and correctly associating attack types with the corresponding tool boundary violations.

In short, fine-tuning improved **behavioral style** (consistent output structure) and **domain-specific classification patterns** (accurate attack type and tool boundary labeling for agentic security scenarios).

---

## 2. What Does RAG Add Over the Fine-Tuned Model Alone?

The fine-tuned model's knowledge is parametric — it is encoded in the model weights during training. This means it can generalize from patterns seen in the training data, but it cannot cite a specific policy rule, reference a current organizational standard, or update its reasoning when policies change without retraining.

RAG addressed this gap. When connected to LangFlow with ChromaDB retrieval over the ToolShield policy source document (`agent_tool_security_policy.md`), the model's recommendations became source-grounded. RAG responses referenced the policy document directly — citing TOOLSHIELD-POL-001 and the retrieved ToolShield policy rules when explaining why a given tool-call sequence violated policy. This kind of citation was not possible from the fine-tuned model alone.

Concretely, RAG improved three things:

- **Factual grounding:** Recommendations were anchored to specific policy rules rather than generated from model priors.
- **Policy alignment:** Answers reflected the retrieved ToolShield policy rules from `agent_tool_security_policy.md` (TOOLSHIELD-POL-001), making them auditable.
- **Explainability:** A response that cites a specific retrieved policy rule is more actionable and trustworthy than one that reaches the same conclusion without naming a source.

---

## 3. When Would You Use a Base Model, Fine-Tuning, or RAG?

**Use a base model** when the task is well within the model's general capabilities and no specialized vocabulary, output format, or domain judgment is required. Base models are appropriate for tasks like general text summarization, broad Q&A, or initial prototyping. They are not appropriate when consistent structured output or domain-specific classification accuracy matters.

**Use fine-tuning** when you need the model to reliably produce a specialized output format, apply a domain-specific classification taxonomy, or behave consistently across a narrow task type. Fine-tuning is the right tool when the behavioral pattern you want is learnable from labeled examples and does not need to change frequently. In this project, the seven-field analyst response format and the agentic security attack taxonomy are both good candidates for fine-tuning.

**Use RAG** when the knowledge the model needs is external, updatable, or needs to be explicitly cited. RAG is the right tool when accuracy depends on matching the current contents of a document, policy, or knowledge base — not just on patterns the model internalized during training. RAG is also appropriate when answers need to be auditable: a user or reviewer can verify a RAG-grounded answer by checking the source document.

**In production, both are useful and complementary.** Fine-tuning ensures the model behaves as a consistent specialist. RAG ensures its reasoning stays aligned with current policy and is explainable. Neither replaces the other.

---

## Limitations and Production Considerations

This project is a focused prototype. Several important production considerations apply:

- **Synthetic dataset:** All 120 training examples were synthetically generated. No real incident data, red team traces, or production tool-call logs were used. A production version would require real labeled examples reviewed by security practitioners.
- **No rigorous evaluation:** Model tier comparisons in this project were qualitative, based on the three fixed test questions. A production deployment would require automated evaluation benchmarks, precision/recall measurement, and adversarial test sets.
- **No access control or monitoring:** A production ToolShield system would need role-based access control for who can query the model, rate limiting, audit logging of all classifications, and alerting when high-confidence malicious sequences are detected.
- **No human approval workflow:** High-risk tool actions (admin grants, bulk email, sensitive file access) must involve a mandatory human approval step. The current project defines this in policy but does not implement it in code.
- **Model size:** `Llama-3.2-3B-Instruct` is a small model chosen for accessibility. A production security analyst model would benefit from a larger base model with stronger reasoning capabilities.

---

## Key Takeaway

This project illustrates the difference between **parametric knowledge** and **contextual knowledge** in a practical AI system. Parametric knowledge is what the model learned and encoded in its weights during training — in this project, the structured analyst output format, the agentic attack taxonomy, and the association between attack types and tool boundaries. This knowledge is always available but fixed at training time and cannot be updated without retraining. Contextual knowledge is what the model receives at inference time via retrieval — in this project, the specific rules from TOOLSHIELD-POL-001 (`agent_tool_security_policy.md`). This knowledge can be updated, extended, and cited without touching the model weights. The most capable production AI systems use both: fine-tuning to instill consistent specialist behavior, and RAG to ground that behavior in current, verifiable, and auditable knowledge. ToolShield Agent demonstrates this pattern at small scale, and the three-tier evaluation makes the contribution of each layer visible and comparable.
