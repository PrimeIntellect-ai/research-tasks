# test_final_state.py
import requests
import subprocess
import struct
import os

def emulate_bytecode(filename):
    reg = [0, 0]
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(3)
            if not chunk or len(chunk) < 3:
                break
            op, arg1, arg2 = struct.unpack("BBB", chunk)
            if op == 0x01: # LOAD_CONST
                reg[arg2] = arg1
            elif op == 0x02: # ADD
                reg[arg2] = (reg[arg2] + reg[arg1]) % 256
            elif op == 0x03: # MUL
                reg[arg2] = (reg[arg2] * reg[arg1]) % 256
            elif op == 0x04: # XOR_CONST
                reg[arg2] = (reg[arg2] ^ arg1) % 256
            elif op == 0xFF: # RETURN
                break
    return reg[1]

def get_expected_checksum(artifact_id):
    # Run the binary to generate output.bin in a temporary directory to avoid conflicts
    cwd = os.getcwd()
    subprocess.run(["/app/legacy_bytecode_gen", str(artifact_id)], cwd=cwd, check=True)
    return emulate_bytecode(os.path.join(cwd, "output.bin"))

def test_unauthorized_missing_header():
    resp = requests.post("http://127.0.0.1:9090/process_artifact", json={"artifact_id": 1})
    assert resp.status_code == 401, f"Expected 401 for missing header, got {resp.status_code}. Response: {resp.text}"

def test_unauthorized_wrong_header():
    headers = {"X-CI-Token": "wrong-token"}
    resp = requests.post("http://127.0.0.1:9090/process_artifact", headers=headers, json={"artifact_id": 1})
    assert resp.status_code == 401, f"Expected 401 for wrong header, got {resp.status_code}. Response: {resp.text}"

def test_valid_request_42():
    expected = get_expected_checksum(42)
    headers = {"X-CI-Token": "build-eng-2024"}
    resp = requests.post("http://127.0.0.1:9090/process_artifact", headers=headers, json={"artifact_id": 42})
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    data = resp.json()
    assert "checksum" in data, f"Response JSON missing 'checksum' key. Response: {data}"
    assert data["checksum"] == expected, f"Expected checksum {expected}, got {data['checksum']}"

def test_valid_request_99():
    expected = get_expected_checksum(99)
    headers = {"X-CI-Token": "build-eng-2024"}
    resp = requests.post("http://127.0.0.1:9090/process_artifact", headers=headers, json={"artifact_id": 99})
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    data = resp.json()
    assert "checksum" in data, f"Response JSON missing 'checksum' key. Response: {data}"
    assert data["checksum"] == expected, f"Expected checksum {expected}, got {data['checksum']}"