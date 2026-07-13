# Data

Contains all dataset files used for fine-tuning and evaluating ToolShield Agent.

## Files

| File | Purpose |
| --- | --- |
| `training_data.jsonl` | Labeled instruction-tuning examples for fine-tuning |
| `test_questions.md` | Fixed 3-question evaluation set used across all three model tiers |

---

## Training Data Schema

Each row in `training_data.jsonl` is a JSON object following the instruction-tuning format:

```json
{
  "instruction": "Analyze the following AI agent tool-call sequence and classify whether it is safe, suspicious, or malicious.",
  "input": "<tool-call sequence in JSON or pseudo-JSON>",
  "output": "<structured analyst response>"
}
```

### Field Descriptions

| Field | Type | Description |
| --- | --- | --- |
| `instruction` | string | Fixed system instruction — same across all rows |
| `input` | string | A JSON or pseudo-JSON representation of an agentic tool-call sequence |
| `output` | string | The expected structured security analyst response |

---

## Structured Output Format

Every `output` value must follow this exact format:

```text
Classification: <safe | suspicious | malicious>
Attack Type: <see enum below>
Tool Boundary Violated: <see enum below>
Risk Reason: <one or two sentences explaining why this is flagged>
Potential Impact: <concrete harm if the sequence executes successfully>
Recommended Control: <specific mitigation or guardrail>
Confidence: <low | medium | high>
```

---

## Enums

### Classification

- `safe`
- `suspicious`
- `malicious`

### Attack Type

- `none`
- `direct_prompt_injection`
- `indirect_prompt_injection`
- `jailbreak_attempt`
- `unauthorized_tool_invocation`
- `sensitive_file_access`
- `privilege_escalation`
- `data_exfiltration`
- `excessive_agency`
- `tool_result_manipulation`

### Tool Boundary Violated

- `email_sending`
- `file_read`
- `file_write`
- `admin_access`
- `external_api_call`
- `database_query`
- `ticket_creation`
- `no_violation`

---

## Input Format Convention

Tool-call sequences in `input` are represented as a JSON array of tool invocation objects:

```json
[
  {
    "tool": "tool_name",
    "args": { "param": "value" },
    "context": "optional description of what triggered this call"
  }
]
```
