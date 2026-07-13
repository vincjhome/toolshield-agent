"""Validate data/training_data.jsonl for ToolShield Agent dataset integrity."""

import json
import sys
from pathlib import Path
from collections import Counter

DATASET_PATH = Path(__file__).parent.parent / "data" / "training_data.jsonl"
EXPECTED_ROWS = 120
REQUIRED_KEYS = {"instruction", "input", "output"}
REQUIRED_OUTPUT_FIELDS = [
    "Classification:",
    "Attack Type:",
    "Tool Boundary Violated:",
    "Risk Reason:",
    "Potential Impact:",
    "Recommended Control:",
    "Confidence:",
]
VALID_CLASSIFICATIONS = {"safe", "suspicious", "malicious"}
VALID_ATTACK_TYPES = {
    "none", "direct_prompt_injection", "indirect_prompt_injection",
    "jailbreak_attempt", "unauthorized_tool_invocation", "sensitive_file_access",
    "privilege_escalation", "data_exfiltration", "excessive_agency",
    "tool_result_manipulation",
}
VALID_TOOL_BOUNDARIES = {
    "email_sending", "file_read", "file_write", "admin_access",
    "external_api_call", "database_query", "ticket_creation", "no_violation",
}


def parse_output_field(output: str, field: str) -> str:
    for line in output.splitlines():
        if line.startswith(field):
            return line[len(field):].strip()
    return ""


def validate():
    errors = []
    warnings = []

    if not DATASET_PATH.exists():
        print(f"ERROR: File not found: {DATASET_PATH}")
        sys.exit(1)

    rows = []
    with open(DATASET_PATH, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
                rows.append((lineno, obj))
            except json.JSONDecodeError as e:
                errors.append(f"Line {lineno}: invalid JSON — {e}")

    print(f"\n{'='*60}")
    print("  ToolShield Agent — Dataset Validation Report")
    print(f"{'='*60}")
    print(f"\nFile: {DATASET_PATH}")
    print(f"Lines parsed: {len(rows)}")

    # Row count
    if len(rows) == EXPECTED_ROWS:
        print(f"Row count:    {len(rows)} / {EXPECTED_ROWS}  [PASS]")
    else:
        errors.append(f"Row count: got {len(rows)}, expected {EXPECTED_ROWS}")
        print(f"Row count:    {len(rows)} / {EXPECTED_ROWS}  [FAIL]")

    classifications = Counter()
    attack_types = Counter()
    tool_boundaries = Counter()
    field_errors = []

    for lineno, obj in rows:
        # Required keys
        missing = REQUIRED_KEYS - obj.keys()
        if missing:
            field_errors.append(f"Line {lineno}: missing keys {missing}")
            continue

        output = obj.get("output", "")

        # Required output fields
        for field in REQUIRED_OUTPUT_FIELDS:
            if field not in output:
                field_errors.append(f"Line {lineno}: output missing '{field}'")

        # Extract and validate enum values
        cls = parse_output_field(output, "Classification:")
        at = parse_output_field(output, "Attack Type:")
        tb = parse_output_field(output, "Tool Boundary Violated:")

        if cls not in VALID_CLASSIFICATIONS:
            field_errors.append(f"Line {lineno}: invalid Classification '{cls}'")
        else:
            classifications[cls] += 1

        if at not in VALID_ATTACK_TYPES:
            field_errors.append(f"Line {lineno}: invalid Attack Type '{at}'")
        else:
            attack_types[at] += 1

        if tb not in VALID_TOOL_BOUNDARIES:
            field_errors.append(f"Line {lineno}: invalid Tool Boundary '{tb}'")
        else:
            tool_boundaries[tb] += 1

    # Classification distribution
    print("\n--- Classification Distribution ---")
    for label in ("safe", "suspicious", "malicious"):
        count = classifications[label]
        status = "PASS" if count == 40 else "WARN"
        print(f"  {label:<12} {count:>3}  (expected 40)  [{status}]")
        if count != 40:
            warnings.append(f"Expected 40 '{label}' examples, got {count}")

    # Attack type distribution
    print("\n--- Attack Type Distribution ---")
    for at, count in sorted(attack_types.items(), key=lambda x: -x[1]):
        print(f"  {at:<35} {count:>3}")

    # Tool boundary distribution
    print("\n--- Tool Boundary Distribution ---")
    for tb, count in sorted(tool_boundaries.items(), key=lambda x: -x[1]):
        print(f"  {tb:<25} {count:>3}")

    # Field-level errors
    all_errors = errors + field_errors
    print(f"\n--- Validation Result ---")
    if all_errors:
        print(f"ERRORS ({len(all_errors)}):")
        for e in all_errors[:20]:
            print(f"  {e}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more")
    else:
        print("  No errors found.")

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")

    print()
    if not all_errors:
        print("RESULT: PASS — dataset is valid.")
    else:
        print("RESULT: FAIL — see errors above.")
    print(f"{'='*60}\n")

    sys.exit(1 if all_errors else 0)


if __name__ == "__main__":
    validate()
