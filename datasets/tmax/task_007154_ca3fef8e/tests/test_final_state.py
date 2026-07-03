# test_final_state.py

import os
import subprocess
import pytest

PIPELINE_SCRIPT = "/home/user/pipeline.sh"
PROCESSOR_CODE = "/home/user/processor.c"
OUTPUT_FILE = "/home/user/sampled_metrics.csv"

def test_files_exist():
    assert os.path.exists(PIPELINE_SCRIPT), f"Missing bash script: {PIPELINE_SCRIPT}"
    assert os.path.isfile(PIPELINE_SCRIPT), f"{PIPELINE_SCRIPT} is not a file."

    assert os.path.exists(PROCESSOR_CODE), f"Missing C program: {PROCESSOR_CODE}"
    assert os.path.isfile(PROCESSOR_CODE), f"{PROCESSOR_CODE} is not a file."

def test_pipeline_executable():
    assert os.access(PIPELINE_SCRIPT, os.X_OK), f"The script {PIPELINE_SCRIPT} is not executable."

def test_pipeline_execution():
    # Remove the output file if it exists to ensure the script generates it fresh
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    try:
        result = subprocess.run(
            [PIPELINE_SCRIPT],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {PIPELINE_SCRIPT} failed with return code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    assert os.path.exists(OUTPUT_FILE), f"The script did not generate {OUTPUT_FILE}."

def test_output_content():
    assert os.path.exists(OUTPUT_FILE), f"Cannot verify content, {OUTPUT_FILE} is missing."

    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        pytest.fail(f"Failed to decode {OUTPUT_FILE} as UTF-8. The output must be valid UTF-8.")

    expected_lines = [
        "500,100,100,défaut ERR-SYS-01 system down",
        "500,200,150,erreur ERR-DBX-99 timeout",
        "502,300,200,fatal ERR-NET-42 connection lost",
        "502,500,400,critique ERR-NET-99 routing failed"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1}.\nExpected: {expected}\nActual:   {actual}"