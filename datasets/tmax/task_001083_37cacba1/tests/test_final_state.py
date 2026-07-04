# test_final_state.py

import os
import hashlib
import re

def test_proto_file_exists_and_valid():
    proto_path = "/home/user/artifacts/build_artifact.proto"
    assert os.path.isfile(proto_path), f"Missing proto file at {proto_path}"

    with open(proto_path, "r") as f:
        content = f.read()

    assert "proto3" in content, "Proto file must use proto3 syntax."
    assert "buildsystem" in content, "Proto file must use package 'buildsystem'."
    assert "enum BuildState" in content, "Proto file must define enum 'BuildState'."
    assert "message Artifact" in content, "Proto file must define message 'Artifact'."

def test_out_directory_and_bins():
    out_dir = "/home/user/artifacts/out"
    assert os.path.isdir(out_dir), f"Directory {out_dir} does not exist."

    expected_bins = ["core_lib.bin", "ui_module.bin", "data_parser.bin"]
    for b in expected_bins:
        bin_path = os.path.join(out_dir, b)
        assert os.path.isfile(bin_path), f"Missing binary file: {bin_path}"

def test_completion_log():
    log_path = "/home/user/artifacts/completion.log"
    assert os.path.isfile(log_path), f"Missing completion log at {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"completion.log should have exactly 3 lines, found {len(lines)}"

    # Check if lines are sorted alphabetically
    assert lines == sorted(lines), "completion.log lines are not sorted alphabetically by filename."

    out_dir = "/home/user/artifacts/out"
    for line in lines:
        match = re.match(r"^([\w_]+\.bin):\s*([a-fA-F0-9]{64})$", line)
        assert match, f"Line in completion.log does not match expected format '<name>.bin: <sha256>': {line}"

        filename, log_hash = match.groups()
        bin_path = os.path.join(out_dir, filename)
        assert os.path.isfile(bin_path), f"File {filename} referenced in completion.log does not exist."

        with open(bin_path, "rb") as bf:
            actual_hash = hashlib.sha256(bf.read()).hexdigest()

        assert log_hash.lower() == actual_hash.lower(), f"Hash mismatch for {filename}. Expected {actual_hash}, got {log_hash}"

def test_test_migrate_exists():
    test_file = "/home/user/artifacts/test_migrate.py"
    assert os.path.isfile(test_file), f"Missing test suite at {test_file}"