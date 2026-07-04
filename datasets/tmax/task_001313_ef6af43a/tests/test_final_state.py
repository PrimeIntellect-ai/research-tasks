# test_final_state.py

import os
import subprocess

def test_diagnostic_report():
    report_path = "/home/user/diagnostic.txt"
    assert os.path.isfile(report_path), f"Diagnostic report missing at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 2, f"Diagnostic report must contain exactly two lines, found {len(lines)}"

    hash_file = "/tmp/bad_commit_hash"
    assert os.path.isfile(hash_file), "Truth data missing: /tmp/bad_commit_hash"

    with open(hash_file, "r") as f:
        expected_hash = f.read().strip()

    assert lines[0] == expected_hash, f"Line 1 of diagnostic.txt is incorrect. Expected {expected_hash}, got {lines[0]}"
    assert lines[1] == "SUCCESS: 1.0", f"Line 2 of diagnostic.txt is incorrect. Expected 'SUCCESS: 1.0', got '{lines[1]}'"

def test_sim_pytest_passes():
    repo_dir = "/home/user/math_sim"
    assert os.path.isdir(repo_dir), f"Directory {repo_dir} is missing"

    result = subprocess.run(
        ["pytest", "test_sim.py"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest test_sim.py failed. Output:\n{result.stdout}\n{result.stderr}"

def test_requirements_fixed():
    req_path = "/home/user/math_sim/requirements.txt"
    assert os.path.isfile(req_path), f"{req_path} is missing"

    with open(req_path, "r") as f:
        content = f.read()

    assert "nonexistent-math-conflict-package" not in content, "requirements.txt still contains the conflicting package 'nonexistent-math-conflict-package'"