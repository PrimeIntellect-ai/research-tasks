# test_final_state.py

import os
import subprocess
from pathlib import Path

def run_graph_filter(target_dir: str) -> dict:
    """
    Runs the student's Rust tool on the specified directory and parses the output.
    Returns a dict mapping filename to 'ACCEPT' or 'REJECT'.
    """
    project_dir = Path("/home/user/graph_filter")
    assert project_dir.is_dir(), f"Rust project directory {project_dir} does not exist."
    assert (project_dir / "Cargo.toml").is_file(), f"Cargo.toml not found in {project_dir}."

    # Run the cargo project
    try:
        result = subprocess.run(
            ["cargo", "run", "--release", "--", target_dir],
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=60,
            check=True
        )
    except subprocess.CalledProcessError as e:
        assert False, f"cargo run failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}"
    except subprocess.TimeoutExpired:
        assert False, "cargo run timed out after 60 seconds."

    # Parse output
    results = {}
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) == 2 and parts[0] in ("ACCEPT", "REJECT"):
            results[parts[1]] = parts[0]

    return results

def test_clean_corpus():
    """Verify that all files in the clean corpus are ACCEPTED."""
    clean_dir = Path("/app/corpora/clean")
    assert clean_dir.is_dir(), f"Clean corpus directory {clean_dir} missing."

    expected_files = {f.name for f in clean_dir.glob("*.txt")}
    assert expected_files, "No text files found in clean corpus."

    results = run_graph_filter(str(clean_dir))

    rejected_files = [f for f, status in results.items() if status == "REJECT"]
    missing_files = expected_files - set(results.keys())

    error_msgs = []
    if rejected_files:
        error_msgs.append(f"{len(rejected_files)} of {len(expected_files)} clean files rejected: {', '.join(rejected_files)}")
    if missing_files:
        error_msgs.append(f"{len(missing_files)} clean files missing from output: {', '.join(missing_files)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_evil_corpus():
    """Verify that all files in the evil corpus are REJECTED."""
    evil_dir = Path("/app/corpora/evil")
    assert evil_dir.is_dir(), f"Evil corpus directory {evil_dir} missing."

    expected_files = {f.name for f in evil_dir.glob("*.txt")}
    assert expected_files, "No text files found in evil corpus."

    results = run_graph_filter(str(evil_dir))

    accepted_files = [f for f, status in results.items() if status == "ACCEPT"]
    missing_files = expected_files - set(results.keys())

    error_msgs = []
    if accepted_files:
        error_msgs.append(f"{len(accepted_files)} of {len(expected_files)} evil files accepted (bypassed): {', '.join(accepted_files)}")
    if missing_files:
        error_msgs.append(f"{len(missing_files)} evil files missing from output: {', '.join(missing_files)}")

    assert not error_msgs, " | ".join(error_msgs)