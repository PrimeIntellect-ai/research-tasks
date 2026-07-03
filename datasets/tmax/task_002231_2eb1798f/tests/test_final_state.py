# test_final_state.py
import os
import glob
import subprocess
import pytest

CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"
SCRIPT_PATH = "/home/user/detect_instability.py"

def run_script(filepath):
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip().split('\n')[-1].strip() if result.stdout else ""
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    assert len(clean_files) > 0, f"No files found in {CLEAN_DIR}"

    failures = []
    for filepath in clean_files:
        output = run_script(filepath)
        if output != "CLEAN":
            failures.append((os.path.basename(filepath), output))

    if failures:
        msg = f"{len(failures)} of {len(clean_files)} clean modified (failed to output CLEAN). Offending files: "
        msg += ", ".join([f"{f} (output: {o})" for f, o in failures[:10]])
        pytest.fail(msg)

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))
    assert len(evil_files) > 0, f"No files found in {EVIL_DIR}"

    failures = []
    for filepath in evil_files:
        output = run_script(filepath)
        if output != "EVIL":
            failures.append((os.path.basename(filepath), output))

    if failures:
        msg = f"{len(failures)} of {len(evil_files)} evil bypassed (failed to output EVIL). Offending files: "
        msg += ", ".join([f"{f} (output: {o})" for f, o in failures[:10]])
        pytest.fail(msg)

def test_makefile_fixed():
    makefile_path = "/app/libstatutils-1.2.0/Makefile"
    if os.path.isfile(makefile_path):
        with open(makefile_path, "r") as f:
            content = f.read()
        assert "-ffast-math" not in content, "The Makefile still contains the unsafe '-ffast-math' flag."