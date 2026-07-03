# test_final_state.py
import os
import glob
import subprocess
import pytest

def run_gatekeeper(csv_path):
    script_path = "/home/user/gatekeeper.py"
    if not os.path.isfile(script_path):
        return None
    try:
        result = subprocess.run(
            ["python3", script_path, csv_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return str(e)

def test_gatekeeper_script_exists():
    script_path = "/home/user/gatekeeper.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_clean_corpus_accepted():
    clean_dir = "/app/corpora/clean"
    csv_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    assert len(csv_files) > 0, f"No CSV files found in {clean_dir}"

    failures = []
    for csv_file in csv_files:
        output = run_gatekeeper(csv_file)
        if output is None:
            pytest.fail("gatekeeper.py script is missing.")
        if "STATUS: ACCEPT" not in output:
            basename = os.path.basename(csv_file)
            failures.append(basename)

    if failures:
        pytest.fail(f"{len(failures)} of {len(csv_files)} clean files rejected or failed: {', '.join(failures)}")

def test_evil_corpus_rejected():
    evil_dir = "/app/corpora/evil"
    csv_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    assert len(csv_files) > 0, f"No CSV files found in {evil_dir}"

    failures = []
    for csv_file in csv_files:
        output = run_gatekeeper(csv_file)
        if output is None:
            pytest.fail("gatekeeper.py script is missing.")
        if "STATUS: REJECT" not in output:
            basename = os.path.basename(csv_file)
            failures.append(basename)

    if failures:
        pytest.fail(f"{len(failures)} of {len(csv_files)} evil files bypassed: {', '.join(failures)}")