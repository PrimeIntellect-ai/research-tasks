# test_final_state.py
import os
import json

def test_security_alerts_log():
    log_path = "/home/user/security_alerts.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert "evil1.tar.gz" in content, "evil1.tar.gz not found in security_alerts.log"
    assert "evil2.zip" in content, "evil2.zip not found in security_alerts.log"
    assert len(content) == 2, f"security_alerts.log should only contain the two malicious files, found: {content}"

def test_storage_report_json():
    json_path = "/home/user/storage_report.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not valid JSON."

    expected = {"alice": 150, "bob": 200, "charlie": 300}

    for key, expected_value in expected.items():
        assert str(key) in data, f"Key '{key}' missing from storage_report.json"
        assert int(data[str(key)]) == expected_value, f"Expected {key} to have {expected_value} bytes, got {data[str(key)]}"

    assert len(data) == len(expected), f"storage_report.json contains unexpected keys. Expected {list(expected.keys())}, got {list(data.keys())}"

def test_extracted_directories():
    assert os.path.isdir("/home/user/extracted/good1") or os.path.isdir("/home/user/extracted/good1.tar.gz"), "good1 archive was not extracted properly."
    assert os.path.isdir("/home/user/extracted/good2") or os.path.isdir("/home/user/extracted/good2.zip"), "good2 archive was not extracted properly."

    assert not os.path.exists("/home/user/extracted/evil1"), "evil1 was maliciously extracted!"
    assert not os.path.exists("/home/user/extracted/evil1.tar.gz"), "evil1 was maliciously extracted!"
    assert not os.path.exists("/home/user/extracted/evil2"), "evil2 was maliciously extracted!"
    assert not os.path.exists("/home/user/extracted/evil2.zip"), "evil2 was maliciously extracted!"