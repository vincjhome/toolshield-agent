# RAG Sources

This directory contains the source documents that form the ToolShield Agent RAG knowledge base. These files are ingested by LangFlow and used to ground the fine-tuned model's security analysis responses in explicit, citable policy and standards content.

---

## Files in This Directory

| File | Purpose |
| --- | --- |
| `agent_tool_security_policy.md` | Internal security policy for AI agent tool usage — the primary policy reference for ToolShield Agent responses |
| `owasp_llm_source_notes.md` | Summarized notes on OWASP LLM Top 10 risks relevant to agentic tool-calling systems |

---

## How These Documents Are Used

### RAG Pipeline Overview

1. Both markdown files are chunked by section (each `##` heading is a natural chunk boundary).
2. Chunks are embedded and stored in a vector store.
3. At inference time, the user's tool-call sequence triggers retrieval of the most relevant chunks.
4. Retrieved chunks are prepended to the prompt as grounding context.
5. The fine-tuned model generates a structured analyst response that can cite the retrieved source.

### Ingestion Instructions for LangFlow

- **File format:** Markdown (`.md`)
- **Recommended chunk strategy:** Split on `##` heading boundaries to preserve semantic units
- **Recommended chunk overlap:** 1 paragraph (to preserve context across section boundaries)
- **Metadata to attach:** `source_file` (filename), `section_title` (heading text), `document_type` (`policy` or `standards_notes`)

### Citation Expectation

RAG-augmented responses from ToolShield Agent should name the source document used. Examples of acceptable citations:

- *"Per TOOLSHIELD-POL-001 Section 6, admin actions require a signed authorization token..."*
- *"This matches the Prompt Injection risk pattern described in the OWASP LLM source notes..."*
- *"Policy Rule 5.2 lists /etc/shadow as a deny-listed path..."*

If the retrieved context did not contribute to the answer, the response should not fabricate a citation.

---

## Scope and Limitations

**These are educational source documents written for the ToolShield Agent prototype, not official production policy.**

Specifically:

- `agent_tool_security_policy.md` is a synthetic policy written for the ToolShield Agent project. It is not a real organizational security policy and has not been reviewed by a legal or security team.
- `owasp_llm_source_notes.md` is a summarized paraphrase of OWASP LLM concepts. It is not an official OWASP publication. Refer to the OWASP LLM Top 10 project at owasp.org for authoritative definitions.
- These documents are designed to demonstrate how RAG grounding improves the specificity and consistency of a fine-tuned security analyst model compared to a base model or fine-tuned-only model.
- Do not use these documents as the basis for real security decisions or compliance programs.
