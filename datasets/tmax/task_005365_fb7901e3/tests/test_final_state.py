# test_final_state.py

import os
import subprocess
from pathlib import Path
import pytest

def test_bad_commit_hash():
    """
    Validates that the user correctly identified the bad commit using git bisect.
    The bad commit is the 3rd commit after v1.0.0.
    """
    repo_dir = "/app/vendored/go-cache-server"
    try:
        # Get the commits after v1.0.0 in chronological order
        output = subprocess.check_output(
            ["git", "rev-list", "--reverse", "v1.0.0..HEAD"],
            cwd=repo_dir, text=True
        )
        commits = [c.strip() for c in output.strip().split('\n') if c.strip()]
        if len(commits) < 3:
            pytest.fail(f"Expected at least 3 commits after v1.0.0, found {len(commits)}")
        expected_bad_commit = commits[2] # 3rd commit (0-indexed)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run git commands in {repo_dir}: {e}")
    except Exception as e:
        pytest.fail(f"Failed to determine expected bad commit from git history: {e}")

    bad_commit_file = Path("/home/user/bad_commit.txt")
    assert bad_commit_file.exists(), f"Expected {bad_commit_file} to exist."
    assert bad_commit_file.is_file(), f"Expected {bad_commit_file} to be a file."

    actual_bad_commit = bad_commit_file.read_text().strip()
    assert actual_bad_commit == expected_bad_commit, \
        f"Incorrect bad commit hash. Expected {expected_bad_commit}, but got {actual_bad_commit}"

def test_go_code_fixed():
    """
    Validates that the source code in the vendored package has been patched
    to fix the goroutine leak.
    """
    repo_dir = "/app/vendored/go-cache-server"
    try:
        result = subprocess.run(
            ["go", "test", "-run", "TestGoroutineLeak", "-v"],
            cwd=repo_dir, capture_output=True, text=True
        )
        assert result.returncode == 0, \
            f"Go test failed, indicating the goroutine leak is not fixed.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"
    except FileNotFoundError:
        pytest.fail("The 'go' command was not found in the environment.")

def test_detector_adversarial_corpus():
    """
    Validates the compiled Go detector against the adversarial corpus.
    Evil files must exit with 1.
    Clean files must exit with 0.
    """
    detector_path = Path("/home/user/detector")
    assert detector_path.exists(), f"Detector executable not found at {detector_path}"
    assert os.access(detector_path, os.X_OK), f"Detector at {detector_path} is not executable."

    evil_dir = Path("/app/corpus/evil")
    clean_dir = Path("/app/corpus/clean")

    assert evil_dir.exists() and evil_dir.is_dir(), f"Evil corpus directory missing at {evil_dir}"
    assert clean_dir.exists() and clean_dir.is_dir(), f"Clean corpus directory missing at {clean_dir}"

    evil_files = [f for f in evil_dir.iterdir() if f.is_file()]
    clean_files = [f for f in clean_dir.iterdir() if f.is_file()]

    assert len(evil_files) > 0, f"No files found in evil corpus directory {evil_dir}"
    assert len(clean_files) > 0, f"No files found in clean corpus directory {clean_dir}"

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run([str(detector_path), str(f)], capture_output=True)
        # Evil files should be rejected (exit code 1)
        if res.returncode != 1:
            evil_bypassed.append(f.name)

    clean_modified = []
    for f in clean_files:
        res = subprocess.run([str(detector_path), str(f)], capture_output=True)
        # Clean files should be preserved/accepted (exit code 0)
        if res.returncode != 0:
            clean_modified.append(f.name)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))