# test_final_state.py

import os
import json
import pytest

def test_audit_report_exists_and_valid():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Audit report {report_path} was not created."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert isinstance(data, list), "The audit report must be a JSON array."
    assert len(data) == 3, f"Expected exactly 3 matching entries, found {len(data)}."

    expected_entries = [
        {
            "timestamp": "2023-10-25T08:15:30Z",
            "decoded_payload": "admin' OR 1=1 --",
            "vulnerable": True
        },
        {
            "timestamp": "2023-10-25T08:16:45Z",
            "decoded_payload": "union select 1,username,323",
            "vulnerable": True
        },
        {
            "timestamp": "2023-10-25T08:25:12Z",
            "decoded_payload": "<script>alert(1)</script>",
            "vulnerable": False
        }
    ]

    for i, expected in enumerate(expected_entries):
        actual = data[i]
        assert actual.get("timestamp") == expected["timestamp"], f"Entry {i} timestamp mismatch. Expected {expected['timestamp']}, got {actual.get('timestamp')}."
        assert actual.get("decoded_payload") == expected["decoded_payload"], f"Entry {i} decoded_payload mismatch. Expected {expected['decoded_payload']}, got {actual.get('decoded_payload')}."
        assert actual.get("vulnerable") is expected["vulnerable"], f"Entry {i} vulnerable mismatch. Expected {expected['vulnerable']}, got {actual.get('vulnerable')}."

def test_rust_project_created():
    project_dir = "/home/user/audit_tool"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    src_main = os.path.join(project_dir, "src", "main.rs")

    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} was not created."
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {project_dir}."
    assert os.path.isfile(src_main), f"src/main.rs not found in {project_dir}."