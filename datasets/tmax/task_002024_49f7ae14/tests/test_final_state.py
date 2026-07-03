# test_final_state.py

import os
import json

def test_migration_report_exists_and_correct():
    file_path = "/home/user/migration_report.json"

    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run the Go program and output to the correct path?"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} does not contain valid JSON."

    assert "rules_to_migrate" in data, "The key 'rules_to_migrate' is missing in the JSON output."

    rules = data["rules_to_migrate"]
    assert isinstance(rules, list), "'rules_to_migrate' should be a list."
    assert len(rules) == 2, f"Expected exactly 2 rules to migrate, but found {len(rules)}. Make sure you are correctly parsing instruction operands to avoid false positives."

    # Sort rules by ID to ensure deterministic checking regardless of output order
    rules_sorted = sorted(rules, key=lambda x: x.get("id", 0))

    rule_b = rules_sorted[0]
    assert rule_b.get("id") == 101, f"Expected rule ID 101, got {rule_b.get('id')}."
    assert rule_b.get("name") == "rule_b", f"Expected rule name 'rule_b', got {rule_b.get('name')}."
    assert rule_b.get("violating_opcodes") == [2, 3], f"Expected violating_opcodes [2, 3] for rule 101, got {rule_b.get('violating_opcodes')}."

    rule_c = rules_sorted[1]
    assert rule_c.get("id") == 102, f"Expected rule ID 102, got {rule_c.get('id')}."
    assert rule_c.get("name") == "rule_c", f"Expected rule name 'rule_c', got {rule_c.get('name')}."
    assert rule_c.get("violating_opcodes") == [5], f"Expected violating_opcodes [5] for rule 102, got {rule_c.get('violating_opcodes')}."