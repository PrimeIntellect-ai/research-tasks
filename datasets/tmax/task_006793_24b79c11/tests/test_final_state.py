# test_final_state.py

import os
import json
import re
import urllib.request
import urllib.error

def test_migration_result_log():
    """Check if the migration_result.log contains the correct JSON result."""
    log_path = "/home/user/migration_result.log"
    assert os.path.exists(log_path), f"File not found: {log_path}"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        assert False, f"Content of {log_path} is not valid JSON: {content}"

    assert "result" in data, f"Key 'result' missing in {log_path}"
    assert data["result"] == 52, f"Expected result 52, got {data['result']}"

def test_protobuf_schema():
    """Check if the protobuf file was generated correctly."""
    proto_path = "/home/user/emulator.proto"
    assert os.path.exists(proto_path), f"File not found: {proto_path}"

    with open(proto_path, 'r') as f:
        content = f.read()

    assert re.search(r'syntax\s*=\s*"proto3"\s*;', content), "Missing or incorrect syntax = 'proto3';"
    assert re.search(r'package\s+emulator\s*;', content), "Missing package emulator;"
    assert re.search(r'service\s+EmulatorService', content), "Missing service EmulatorService"
    assert re.search(r'rpc\s+ExecuteProgram', content), "Missing rpc ExecuteProgram"
    assert re.search(r'string\s+program\s*=\s*1\s*;', content), "Missing string program = 1;"
    assert re.search(r'int32\s+result\s*=\s*1\s*;', content), "Missing int32 result = 1;"

def test_script_executable():
    """Check if test script is executable."""
    script_path = "/home/user/test_system.sh"
    assert os.path.exists(script_path), f"File not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_live_service():
    """Check if nginx and the python server are running and correctly proxying."""
    url = "http://127.0.0.1:8080/execute"
    payload = json.dumps({"program": "2 3 ADD"}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            try:
                data = json.loads(body)
                assert data.get("result") == 5, f"Expected result 5 for '2 3 ADD', got {data.get('result')}"
            except json.JSONDecodeError:
                assert False, f"Response body is not valid JSON: {body}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx on 127.0.0.1:8080: {e}"