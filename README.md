# ToolShield Agent

ToolShield Agent is a domain-specialized AI security analyst that classifies AI agent tool-call sequences as **safe**, **suspicious**, or **malicious**. It detects attack patterns including prompt injection, unauthorized tool invocations, sensitive file access, privilege escalation, and data exfiltration through agentic tools.

The project demonstrates a three-tier progressive evaluation: base model → LoRA fine-tuned model → fine-tuned model with retrieval-augmented generation (RAG). Each tier adds a measurable layer of domain capability.

---

## Three-Tier Architecture

| Tier | Configuration | What It Demonstrates |
| --- | --- | --- |
| Base | `unsloth/Llama-3.2-3B-Instruct`, no adaptation | Detection floor without domain specialization |
| Fine-Tuned | LoRA-adapted on 120 synthetic security examples | Consistent structured output, attack taxonomy accuracy |
| Fine-Tuned + RAG | Fine-tuned model via Ollama + LangFlow + ChromaDB | Policy-grounded, source-citable threat analysis |

---

## Structured Analyst Output

Every classification produces a fixed seven-field response:

```text
Classification: malicious
Attack Type: indirect_prompt_injection
Tool Boundary Violated: email_sending
Risk Reason: ...
Potential Impact: ...
Recommended Control: ...
Confidence: high
```

---

## Project Structure

```text
data/                # Training dataset (120 JSONL examples) and evaluation test questions
docs/                # Project plan and architecture documentation
langflow_workspace/  # LangFlow workflow (LangFlow_ToolShield_Agent_RAG.json)
models/              # Ollama Modelfile for local deployment
notebooks/           # Fine-tuning notebook (Unsloth/LoRA, Colab)
outputs/             # Model response comparisons across all three tiers
rag_sources/         # Source documents for the RAG knowledge base
screenshots/         # Visual captures across all three model tiers
scripts/             # JSONL validation utility
reflection.md        # Project reflection: base model vs fine-tuned vs RAG
```

---

## Classification Taxonomy

**Labels:** `safe` | `suspicious` | `malicious`

**Attack Types:**

| Value | Description |
| --- | --- |
| `none` | No attack detected |
| `direct_prompt_injection` | Malicious instructions in user message or system prompt |
| `indirect_prompt_injection` | Malicious instructions embedded in tool results or external content |
| `jailbreak_attempt` | Persona or roleplay exploit to bypass restrictions |
| `unauthorized_tool_invocation` | Tool called outside its authorized scope |
| `sensitive_file_access` | Access to deny-listed system paths or credentials |
| `privilege_escalation` | Attempt to acquire elevated permissions |
| `data_exfiltration` | Data routed to an unauthorized external destination |
| `excessive_agency` | Agent takes unsolicited consequential actions |
| `tool_result_manipulation` | Attacker-controlled tool results used to influence behavior |

**Tool Boundaries:** `email_sending`, `file_read`, `file_write`, `admin_access`, `external_api_call`, `database_query`, `ticket_creation`, `no_violation`

---

## RAG Knowledge Base

The RAG tier retrieves from two source documents in `rag_sources/`:

- `agent_tool_security_policy.md` — internal tool security policy (TOOLSHIELD-POL-001)
- `owasp_llm_source_notes.md` — OWASP LLM Top 10 risk notes for agentic systems

Ingested via LangFlow with ChromaDB vector store. Recommended chunk boundary: `##` headings.

---

## Local Deployment

The fine-tuned model is served via Ollama. The GGUF model file is not included in this repository (1.9 GB). Download separately and run:

```bash
# Place the GGUF in models/toolshield-agent-gguf/ then:
ollama create toolshield-agent -f models/toolshield-agent-gguf/Modelfile
ollama run toolshield-agent
```

---

## Validation

```bash
python scripts/validate_jsonl.py
```

Validates all 120 JSONL examples: JSON integrity, classification distribution (40/40/40), required fields, and enum values.

---

## Technical Stack

| Component | Technology |
| --- | --- |
| Base model | `unsloth/Llama-3.2-3B-Instruct` |
| Fine-tuning | Unsloth + LoRA (Google Colab) |
| Local inference | Ollama |
| RAG pipeline | LangFlow + ChromaDB |
| Vector store | ChromaDB |
