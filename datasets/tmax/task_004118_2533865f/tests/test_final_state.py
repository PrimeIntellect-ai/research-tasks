# test_final_state.py
import os
import json
import shutil
import subprocess
import time
import re
import pytest

def test_curator_performance_and_correctness():
    source_file = "/home/user/curator.go"
    assert os.path.exists(source_file), f"Source file {source_file} does not exist"

    # Clean up repo directory to ensure a fresh run
    repo_dir = "/home/user/repo"
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    os.makedirs(repo_dir, exist_ok=True)

    # Compile the Go program
    binary_path = "/tmp/curator"
    compile_cmd = ["go", "build", "-o", binary_path, source_file]
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile Go program:\n{e.stderr}")

    # Run and measure time
    start_time = time.time()
    try:
        subprocess.run([binary_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of compiled binary failed:\n{e.stderr}")

    end_time = time.time()
    runtime_seconds = end_time - start_time

    # Assert execution time
    assert runtime_seconds <= 3.0, f"Execution time {runtime_seconds:.2f}s exceeded the 3.0s threshold"

    # Validate manifest.json
    manifest_path = os.path.join(repo_dir, "manifest.json")
    assert os.path.exists(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("manifest.json is not valid JSON")

    assert "total_frames" in manifest, "total_frames missing in manifest"
    assert manifest["total_frames"] == 150, f"Expected total_frames to be 150, got {manifest['total_frames']}"

    assert "artifacts" in manifest, "artifacts array missing in manifest"
    assert len(manifest["artifacts"]) == 150, f"Expected 150 artifacts, got {len(manifest['artifacts'])}"

    # Validate audit.log
    audit_path = os.path.join(repo_dir, "audit.log")
    assert os.path.exists(audit_path), f"Audit log missing at {audit_path}"

    with open(audit_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Each block is 4 lines, so 150 blocks * 4 lines = 600 lines
    assert len(lines) == 600, f"Expected 600 non-empty lines in audit.log, got {len(lines)}. Interleaved or missing entries?"

    frame_numbers = set()
    for i in range(0, len(lines), 4):
        begin_line = lines[i]
        size_line = lines[i+1]
        status_line = lines[i+2]
        end_line = lines[i+3]

        begin_match = re.match(r"^BEGIN FRAME (\d+)$", begin_line)
        assert begin_match, f"Invalid BEGIN FRAME line at line {i+1}: {begin_line}"
        frame_number = int(begin_match.group(1))
        frame_numbers.add(frame_number)

        assert re.match(r"^SIZE: \d+$", size_line), f"Invalid SIZE line at line {i+2}: {size_line}"
        assert status_line == "STATUS: PROCESSED", f"Invalid STATUS line at line {i+3}: {status_line}"
        assert end_line == "END FRAME", f"Invalid END FRAME line at line {i+4}: {end_line}"

    assert len(frame_numbers) == 150, f"Expected 150 unique frames in audit.log, found {len(frame_numbers)}"