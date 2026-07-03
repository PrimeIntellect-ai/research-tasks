# test_final_state.py

import os
import requests
import pytest

def test_api_snap1():
    url = "http://127.0.0.1:9090/api/v1/inspect"
    payload = {"filepath": "/home/user/spool/snap1.enc"}
    try:
        resp = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Body: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get("volume") == "vol-X1", f"Expected volume 'vol-X1', got {data.get('volume')}"
    usage = data.get("usage_percent")
    assert usage is not None, "Missing 'usage_percent' in response"
    assert abs(float(usage) - 25.0) < 0.01, f"Expected usage_percent ~25.0, got {usage}"

def test_api_snap2():
    url = "http://127.0.0.1:9090/api/v1/inspect"
    payload = {"filepath": "/home/user/spool/snap2.enc"}
    try:
        resp = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Body: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get("volume") == "vol-Y2", f"Expected volume 'vol-Y2', got {data.get('volume')}"
    usage = data.get("usage_percent")
    assert usage is not None, "Missing 'usage_percent' in response"
    assert abs(float(usage) - 50.0) < 0.01, f"Expected usage_percent ~50.0, got {usage}"

def test_audit_log():
    audit_file = "/home/user/audit.csv"
    assert os.path.exists(audit_file), f"Audit log {audit_file} does not exist. Did the service create it?"

    with open(audit_file, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n") if line.strip()]

    assert len(lines) >= 3, "Audit log should have a header and at least 2 entries (from the tests just run)"
    assert lines[0] == "timestamp,volume,usage_percent", f"Incorrect header in audit.csv: {lines[0]}"

    found_snap1 = False
    found_snap2 = False

    for line in lines[1:]:
        parts = line.split(",")
        if len(parts) == 3:
            vol = parts[1]
            pct = parts[2]
            if vol == "vol-X1" and (pct.startswith("25.") or pct == "25"):
                found_snap1 = True
            if vol == "vol-Y2" and (pct.startswith("50.") or pct == "50"):
                found_snap2 = True

    assert found_snap1, "Audit log missing entry for vol-X1 with ~25% usage"
    assert found_snap2, "Audit log missing entry for vol-Y2 with ~50% usage"