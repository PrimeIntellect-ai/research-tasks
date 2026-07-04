# test_final_state.py

import os
import json
import ast

WORKSPACE_DIR = "/home/user/workspace"
REDACTOR_FILE = os.path.join(WORKSPACE_DIR, "redactor.py")
SCHEMA_PB2_FILE = os.path.join(WORKSPACE_DIR, "schema_pb2.py")
REDACTED_FILE = os.path.join(WORKSPACE_DIR, "redacted.jsonl")
SUMMARY_FILE = os.path.join(WORKSPACE_DIR, "summary.json")

def test_protobuf_compiled():
    assert os.path.isfile(SCHEMA_PB2_FILE), f"Protobuf compiled file missing: {SCHEMA_PB2_FILE}"

def test_redactor_script_exists_and_valid():
    assert os.path.isfile(REDACTOR_FILE), f"Redactor script missing: {REDACTOR_FILE}"

    with open(REDACTOR_FILE, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {REDACTOR_FILE}: {e}")

    trie_class_found = False
    methods_found = set()

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "TokenTrie":
            trie_class_found = True
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods_found.add(item.name)

    assert trie_class_found, "Class 'TokenTrie' not found in redactor.py"
    assert "add_token" in methods_found, "Method 'add_token' not found in TokenTrie class"
    assert "redact" in methods_found, "Method 'redact' not found in TokenTrie class"

def test_summary_json():
    assert os.path.isfile(SUMMARY_FILE), f"Summary file missing: {SUMMARY_FILE}"
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {SUMMARY_FILE}")

    assert "total_redactions" in data, "Key 'total_redactions' missing in summary.json"
    assert data["total_redactions"] == 6, f"Expected 6 total redactions, got {data['total_redactions']}"

def test_redacted_jsonl():
    assert os.path.isfile(REDACTED_FILE), f"Redacted file missing: {REDACTED_FILE}"

    expected_lines = [
        {"id": "1", "user_agent": "Mozilla [REDACTED] client", "request_payload": "login [REDACTED]", "status_code": 200, "response_payload": "ok"},
        {"id": "2", "user_agent": "curl/7.68.0", "request_payload": "query data", "status_code": 403, "response_payload": "Missing [REDACTED] or [REDACTED]"},
        {"id": "3", "user_agent": "PostmanRuntime/7.28", "request_payload": "auth [REDACTED] and [REDACTED]", "status_code": 200, "response_payload": "success"}
    ]

    with open(REDACTED_FILE, "r", encoding="utf-8") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"Expected 3 lines in redacted.jsonl, got {len(lines)}"

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON on line {i+1} of {REDACTED_FILE}")

        assert data == expected_lines[i], f"Mismatch on line {i+1} of {REDACTED_FILE}. Expected {expected_lines[i]}, got {data}"