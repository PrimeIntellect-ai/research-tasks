# test_final_state.py
import os
import json
import pytest

def test_investigation_summary_exists():
    path = "/home/user/investigation_summary.json"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

def test_investigation_summary_content():
    path = "/home/user/investigation_summary.json"
    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "sqli_line" in data, "Key 'sqli_line' missing from JSON."
    assert "xss_line" in data, "Key 'xss_line' missing from JSON."
    assert "root_ca_cn" in data, "Key 'root_ca_cn' missing from JSON."

    assert data["sqli_line"] == 10, f"Expected sqli_line to be 10, got {data['sqli_line']}."
    assert data["xss_line"] == 19, f"Expected xss_line to be 19, got {data['xss_line']}."
    assert data["root_ca_cn"] == "EvilCorp Root CA", f"Expected root_ca_cn to be 'EvilCorp Root CA', got {data['root_ca_cn']}."

def test_original_artifacts_unmodified():
    # Verify the artifacts are still present
    assert os.path.isfile("/home/user/incident/app.py"), "Original app.py was removed or renamed."
    assert os.path.isfile("/home/user/incident/cert_chain.pem"), "Original cert_chain.pem was removed or renamed."