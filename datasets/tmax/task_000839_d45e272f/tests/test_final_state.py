# test_final_state.py
import os
import subprocess
import pytest

def test_filter_go_exists():
    assert os.path.isfile("/home/user/filter.go"), "The Go program /home/user/filter.go does not exist."

def test_clean_corpus_accepted():
    clean_dir = "/app/corpus/clean/"
    if not os.path.isdir(clean_dir):
        pytest.skip(f"Clean corpus directory {clean_dir} not found.")

    csv_files = [f for f in os.listdir(clean_dir) if f.endswith(".csv")]
    if not csv_files:
        pytest.skip(f"No CSV files found in {clean_dir}.")

    result = subprocess.run(
        ["go", "run", "/home/user/filter.go", clean_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Go program failed when running on clean corpus. Stderr: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    rejected_files = []
    accepted_files = []

    for line in output_lines:
        parts = line.split()
        if len(parts) == 2:
            status, filename = parts[0], parts[1]
            if status == "ACCEPT":
                accepted_files.append(filename)
            elif status == "REJECT":
                rejected_files.append(filename)

    # Verify all clean files are accepted
    missing_accepted = [f for f in csv_files if f not in accepted_files]

    error_msg = f"{len(rejected_files)} of {len(csv_files)} clean files rejected. "
    if rejected_files:
        error_msg += f"Offending files: {', '.join(rejected_files[:5])}. "
    if missing_accepted:
        error_msg += f"Missing from ACCEPT output: {', '.join(missing_accepted[:5])}."

    assert not rejected_files and not missing_accepted, error_msg

def test_evil_corpus_rejected():
    evil_dir = "/app/corpus/evil/"
    if not os.path.isdir(evil_dir):
        pytest.skip(f"Evil corpus directory {evil_dir} not found.")

    csv_files = [f for f in os.listdir(evil_dir) if f.endswith(".csv")]
    if not csv_files:
        pytest.skip(f"No CSV files found in {evil_dir}.")

    result = subprocess.run(
        ["go", "run", "/home/user/filter.go", evil_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Go program failed when running on evil corpus. Stderr: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    rejected_files = []
    accepted_files = []

    for line in output_lines:
        parts = line.split()
        if len(parts) == 2:
            status, filename = parts[0], parts[1]
            if status == "REJECT":
                rejected_files.append(filename)
            elif status == "ACCEPT":
                accepted_files.append(filename)

    # Verify all evil files are rejected
    missing_rejected = [f for f in csv_files if f not in rejected_files]

    error_msg = f"{len(accepted_files)} of {len(csv_files)} evil files accepted (bypassed). "
    if accepted_files:
        error_msg += f"Offending files: {', '.join(accepted_files[:5])}. "
    if missing_rejected:
        error_msg += f"Missing from REJECT output: {', '.join(missing_rejected[:5])}."

    assert not accepted_files and not missing_rejected, error_msg