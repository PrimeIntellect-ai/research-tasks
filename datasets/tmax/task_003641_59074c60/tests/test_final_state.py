# test_final_state.py
import os
import json
import subprocess
import pytest

PIPELINE_DIR = "/home/user/legacy_pipeline"
VENV_PYTHON = "/home/user/venv/bin/python"
VENV_PIP = "/home/user/venv/bin/pip"
REPORT_PATH = "/home/user/debug_report.json"

def test_venv_and_dependencies():
    assert os.path.exists(VENV_PYTHON), "Virtual environment python not found at /home/user/venv/bin/python"

    # Check if requests and urllib3 are installed
    out = subprocess.check_output([VENV_PIP, "list"]).decode()
    assert "requests" in out.lower(), "requests is not installed in the venv"
    assert "urllib3" in out.lower(), "urllib3 is not installed in the venv"

    # Check for conflicts
    try:
        subprocess.check_output([VENV_PIP, "check"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"pip check failed, indicating dependency conflicts: {e.output.decode()}")

def test_makefile_and_compilation():
    makefile_path = os.path.join(PIPELINE_DIR, "Makefile")
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-lm" in content, "Makefile does not contain the required -lm linker flag"

    so_path = os.path.join(PIPELINE_DIR, "libfastcompute.so")
    assert os.path.exists(so_path), "libfastcompute.so was not built"

def test_debug_report():
    assert os.path.exists(REPORT_PATH), f"{REPORT_PATH} does not exist"
    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("debug_report.json is not valid JSON")

    assert report.get("missing_linker_flag") == "-lm", "missing_linker_flag is incorrect"
    assert report.get("crashing_string_length") == 128, "crashing_string_length is incorrect"
    assert report.get("race_condition_variable") == "total_score", "race_condition_variable is incorrect"

def test_process_data_execution():
    script_path = os.path.join(PIPELINE_DIR, "process_data.py")

    # Check for Lock or synchronization in source code
    with open(script_path, "r") as f:
        content = f.read()

    assert "Lock" in content or "Semaphore" in content or "RLock" in content or "mutex" in content.lower(), "process_data.py does not seem to use a lock for synchronization"
    assert "127" in content or "[:127]" in content, "process_data.py does not seem to truncate the string to 127 bytes to prevent buffer overflow"

    # Run the script multiple times to ensure deterministic output and no segfaults
    outputs = set()
    for _ in range(3):
        try:
            out = subprocess.check_output([VENV_PYTHON, script_path], stderr=subprocess.STDOUT, cwd=PIPELINE_DIR).decode()

            # Extract the final score line
            score_line = next((line for line in out.splitlines() if "Final Score:" in line), None)
            assert score_line is not None, "process_data.py did not output 'Final Score:'"
            outputs.add(score_line.strip())
        except subprocess.CalledProcessError as e:
            pytest.fail(f"process_data.py crashed or returned non-zero exit code: {e.output.decode()}")

    assert len(outputs) == 1, f"process_data.py output is not deterministic (race condition not properly fixed). Outputs seen: {outputs}"