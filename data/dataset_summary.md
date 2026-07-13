# Dataset Summary

## Purpose

This dataset is the synthetic instruction-tuning corpus for ToolShield Agent — a fine-tuned AI security analyst that classifies AI agent tool-call sequences as `safe`, `suspicious`, or `malicious` and produces structured analyst responses covering attack type, tool boundary violated, risk reasoning, potential impact, recommended controls, and confidence level.

**Important:** This is synthetic data generated for demonstration purposes. It is not a production-grade detection dataset and has not been derived from real incident data or validated by security practitioners.

---

## Label Distribution

| Classification | Count | Share |
| --- | --- | --- |
| `safe` | 40 | 33.3% |
| `suspicious` | 40 | 33.3% |
| `malicious` | 40 | 33.3% |

**Total:** 120 examples

The balanced 40/40/40 split ensures the model does not develop a prior bias toward any single classification. Real deployment datasets would likely be imbalanced (more safe than malicious), but balance is appropriate here for learning the full decision boundary.

---

## Attack Type Distribution

| Attack Type | Count |
| --- | --- |
| `none` | 80 |
| `direct_prompt_injection` | 5 |
| `indirect_prompt_injection` | 5 |
| `jailbreak_attempt` | 5 |
| `sensitive_file_access` | 5 |
| `privilege_escalation` | 5 |
| `data_exfiltration` | 5 |
| `unauthorized_tool_invocation` | 4 |
| `excessive_agency` | 3 |
| `tool_result_manipulation` | 3 |

The 80 `none` examples cover safe examples (all `none`) and suspicious examples (most `none`, since the suspicious class is characterized by ambiguous risk rather than a confirmed attack type).

---

## Tool Boundary Distribution

| Tool Boundary | Count |
| --- | --- |
| `no_violation` | 40 |
| `file_read` | 15 |
| `admin_access` | 14 |
| `database_query` | 13 |
| `external_api_call` | 13 |
| `email_sending` | 11 |
| `file_write` | 9 |
| `ticket_creation` | 5 |

`no_violation` exactly matches the 40 safe examples. The remaining 80 examples distribute across all seven boundary types, with higher-risk boundaries (`file_read`, `admin_access`, `database_query`) appearing more frequently to reflect their role in common attack chains.

---

## Tool Coverage

The dataset uses the following agent tools across examples:

| Tool | Role in Dataset |
| --- | --- |
| `read_email` | Safe inbox access; indirect injection vector |
| `send_email` | Safe user-directed sends; exfiltration channel |
| `read_file` | Safe doc access; sensitive file attack vector |
| `write_file` | Safe report writes; system file abuse vector |
| `create_ticket` | Safe ticketing; XSS, PII leakage, and exfil vector |
| `query_database` | Safe analytics; exfiltration, SQLi, and DDL abuse |
| `call_external_api` | Safe public APIs; exfiltration and injection vector |
| `admin_grant_access` | Safe with proper auth; privilege escalation target |
| `summarize_document` | Safe summarization; injection and exfil vector |
| `retrieve_policy` | Safe policy lookup; read-only, low risk |

---

## What the Model Should Learn

**From safe examples:**

- Recognize normal business workflows (report generation, inbox summarization, analytics queries, policy lookups) as safe.
- Identify signals of authorization: user-specified recipients, designated directories, bounded queries, signed tokens.
- Produce consistent seven-field analyst output with `none` / `no_violation` / `high` confidence for clear safe cases.

**From suspicious examples:**

- Recognize ambiguous signals: unusual file paths, broad database queries, external API calls with user data, bulk access without clear purpose.
- Distinguish "needs review" from "confirmed malicious" — suspicious examples have `medium` or `low` confidence with specific investigation recommendations.
- Identify when context is missing (no user request logged, no auth token present) as a risk signal in itself.

**From malicious examples:**

- Map specific attack patterns to the correct `attack_type` enum value.
- Identify the exact `tool_boundary_violated` for each attack.
- Articulate concrete `potential_impact` and specific `recommended_control` rather than vague responses.
- Understand that unsigned in-context messages, jailbreak personas, and content embedded in tool results are categorically different from legitimate user instructions.

---

## Synthetic Data Notice

All examples in this dataset are synthetically generated for demonstration purposes. Specifically:

- No real secrets, API keys, credentials, or personal data are included.
- Attack scenarios are illustrative constructions, not transcripts of real incidents.
- The dataset has not been reviewed by a security practitioner for completeness or accuracy.
- It is not intended for use in any production threat detection system.
- The three final test questions in `test_questions.md` are excluded from this training set to preserve evaluation integrity.
