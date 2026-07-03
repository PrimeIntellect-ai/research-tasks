# test_final_state.py
import os
import json
import socket
import pytest
import math

def test_proto_file():
    proto_path = "/home/user/artifact.proto"
    assert os.path.exists(proto_path), f"File {proto_path} does not exist."

    with open(proto_path, "r") as f:
        content = f.read()

    assert "package build;" in content, "Proto file is missing 'package build;'"
    assert "service ArtifactCache" in content, "Proto file is missing 'service ArtifactCache'"
    assert "rpc GetChecksum" in content, "Proto file is missing 'rpc GetChecksum'"
    assert "ArtifactRequest" in content, "Proto file is missing 'ArtifactRequest'"
    assert "ArtifactResponse" in content, "Proto file is missing 'ArtifactResponse'"

def test_certs_exist():
    crt_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"
    assert os.path.exists(crt_path), f"Certificate file {crt_path} does not exist."
    assert os.path.exists(key_path), f"Key file {key_path} does not exist."

def test_json_output():
    json_path = "/home/user/tls_overhead.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "plaintext_rps" in data, "JSON missing 'plaintext_rps'"
    assert "tls_rps" in data, "JSON missing 'tls_rps'"
    assert "overhead_percentage" in data, "JSON missing 'overhead_percentage'"

    # Verify the math roughly
    pt = float(data["plaintext_rps"])
    tls = float(data["tls_rps"])
    overhead = float(data["overhead_percentage"])

    if pt > 0:
        expected_overhead = ((pt - tls) / pt) * 100
        assert math.isclose(overhead, expected_overhead, rel_tol=0.01), f"overhead_percentage {overhead} does not match expected {expected_overhead}"

def test_ports_in_use():
    for port in [50051, 50052]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"Port {port} is not listening. The gRPC server must be running."