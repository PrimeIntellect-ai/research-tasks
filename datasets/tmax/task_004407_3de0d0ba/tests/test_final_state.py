# test_final_state.py
import os
import json
import pytest

def test_parser_bin_exists():
    bin_path = "/home/user/build_tools/parser_bin"
    assert os.path.isfile(bin_path), f"Expected compiled binary at {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"The file {bin_path} is not executable."

def test_protobuf_file():
    proto_path = "/home/user/pipeline/build_service.proto"
    assert os.path.isfile(proto_path), f"Protobuf file {proto_path} does not exist."
    with open(proto_path, 'r') as f:
        content = f.read()
    assert "DependencyResolver" in content, "Service DependencyResolver not found in proto file."
    assert "ResolveBuild" in content, "RPC method ResolveBuild not found in proto file."
    assert "ResolveRequest" in content, "Message ResolveRequest not found in proto file."
    assert "ResolveResponse" in content, "Message ResolveResponse not found in proto file."

def test_resolution_json():
    json_path = "/home/user/pipeline/resolution.json"
    assert os.path.isfile(json_path), f"Output JSON file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "versions" in data, "Key 'versions' missing from JSON."
    assert "score" in data, "Key 'score' missing from JSON."

    versions = data["versions"]
    score = data["score"]

    c = versions.get("Core")
    u = versions.get("UI")
    n = versions.get("Network")
    d = versions.get("Database")

    assert c in {1, 2, 3}, f"Core version {c} is not in allowed set {{1, 2, 3}}"
    assert u in {1, 2}, f"UI version {u} is not in allowed set {{1, 2}}"
    assert n in {2, 3}, f"Network version {n} is not in allowed set {{2, 3}}"
    assert d in {1, 2, 3}, f"Database version {d} is not in allowed set {{1, 2, 3}}"

    assert n == d, f"Network ({n}) and Database ({d}) versions must match."
    assert sum([c, u, n, d]) == 9, f"Sum of versions must be 9, got {sum([c, u, n, d])}."

    if u == 2:
        assert c >= 2, f"If UI=2, Core must be >= 2. Got Core={c}."

    expected_score = (c * 1.5) + (u * 2.5) + (n * 3.5) + (d * 4.5)
    assert float(score) == expected_score, f"Expected score {expected_score}, got {score}."