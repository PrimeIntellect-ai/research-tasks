# test_final_state.py

import os
import subprocess
import pytest

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr

def test_vendored_library_compiles():
    vendored_dir = "/app/vendored/graph-mapper"
    assert os.path.isdir(vendored_dir), f"Vendored library directory {vendored_dir} does not exist."

    cargo_toml = os.path.join(vendored_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"{cargo_toml} does not exist."

    with open(cargo_toml, "r") as f:
        content = f.read()
        assert "serde" in content, "The 'serde' dependency is still missing from graph-mapper/Cargo.toml."

    # Check if it compiles
    stdout, stderr = run_command(["cargo", "check"], cwd=vendored_dir)
    if "error" in stderr.lower():
        pytest.fail(f"graph-mapper failed to compile:\n{stderr}")

def test_record_validator_compiles():
    validator_dir = "/home/user/record-validator"
    assert os.path.isdir(validator_dir), f"Validator directory {validator_dir} does not exist."

    cargo_toml = os.path.join(validator_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"{cargo_toml} does not exist."

    # Build the CLI
    stdout, stderr = run_command(["cargo", "build", "--release"], cwd=validator_dir)
    if "error" in stderr.lower():
        pytest.fail(f"record-validator failed to compile:\n{stderr}")

def test_validator_on_clean_corpus():
    validator_dir = "/home/user/record-validator"
    clean_dir = "/app/data/clean_corpus"

    stdout, stderr = run_command(["cargo", "run", "--release", "--", clean_dir], cwd=validator_dir)

    output_lines = stdout.strip().split("\n")
    results = {}
    for line in output_lines:
        line = line.strip()
        if not line: continue
        parts = line.split()
        if len(parts) >= 2:
            status, filename = parts[0], parts[1]
            results[filename] = status

    expected_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]

    rejected_files = []
    missing_files = []

    for f in expected_files:
        if f not in results:
            missing_files.append(f)
        elif results[f] != "ACCEPT":
            rejected_files.append(f)

    error_msg = []
    if rejected_files:
        error_msg.append(f"{len(rejected_files)} of {len(expected_files)} clean modified (rejected instead of accepted): {', '.join(rejected_files)}")
    if missing_files:
        error_msg.append(f"{len(missing_files)} clean files missing from output: {', '.join(missing_files)}")

    if error_msg:
        pytest.fail("; ".join(error_msg))

def test_validator_on_evil_corpus():
    validator_dir = "/home/user/record-validator"
    evil_dir = "/app/data/evil_corpus"

    stdout, stderr = run_command(["cargo", "run", "--release", "--", evil_dir], cwd=validator_dir)

    output_lines = stdout.strip().split("\n")
    results = {}
    for line in output_lines:
        line = line.strip()
        if not line: continue
        parts = line.split()
        if len(parts) >= 2:
            status, filename = parts[0], parts[1]
            results[filename] = status

    expected_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]

    accepted_files = []
    missing_files = []

    for f in expected_files:
        if f not in results:
            missing_files.append(f)
        elif results[f] != "REJECT":
            accepted_files.append(f)

    error_msg = []
    if accepted_files:
        error_msg.append(f"{len(accepted_files)} of {len(expected_files)} evil bypassed (accepted instead of rejected): {', '.join(accepted_files)}")
    if missing_files:
        error_msg.append(f"{len(missing_files)} evil files missing from output: {', '.join(missing_files)}")

    if error_msg:
        pytest.fail("; ".join(error_msg))