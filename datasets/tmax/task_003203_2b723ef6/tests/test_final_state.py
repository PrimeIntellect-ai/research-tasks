# test_final_state.py

import os
import subprocess
import pytest

PIPELINE_DIR = "/home/user/pipeline"
SRC_DIR = os.path.join(PIPELINE_DIR, "src")
RECOVERED_DAT = os.path.join(PIPELINE_DIR, "recovered.dat")
POISON_TXT = "/home/user/poison.txt"
BUILD_FLAG = os.path.join(PIPELINE_DIR, "build_success.flag")
AGGREGATE_AWK = os.path.join(PIPELINE_DIR, "aggregate.awk")
METRICS_TXT = os.path.join(PIPELINE_DIR, "metrics.txt")

def test_phase1_recovered_dat():
    assert os.path.isfile(RECOVERED_DAT), f"Phase 1 failed: {RECOVERED_DAT} is missing."

    with open(RECOVERED_DAT, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "SET config_path /etc/default",
        "SET max_workers 4",
        "SET retries 5",
        "SET feature_flag true"
    ]
    expected_content = "\n".join(expected_lines)

    assert content == expected_content, f"Phase 1 failed: {RECOVERED_DAT} does not contain the exact expected valid transactions."

def test_phase2_poison_file_identified_and_removed():
    assert os.path.isfile(POISON_TXT), f"Phase 2 failed: {POISON_TXT} is missing."

    with open(POISON_TXT, "r") as f:
        poison_content = f.read().strip()

    assert poison_content == "file_314.src", f"Phase 2 failed: {POISON_TXT} contains '{poison_content}', expected 'file_314.src'."

    poisoned_src_path = os.path.join(SRC_DIR, "file_314.src")
    assert not os.path.exists(poisoned_src_path), f"Phase 2 failed: Poisoned file {poisoned_src_path} was not deleted from the src/ directory."

def test_phase3_aggregate_awk_fixed():
    assert os.path.isfile(AGGREGATE_AWK), f"{AGGREGATE_AWK} is missing."
    assert os.path.isfile(METRICS_TXT), f"{METRICS_TXT} is missing."

    try:
        result = subprocess.run(
            ["awk", "-f", AGGREGATE_AWK, METRICS_TXT],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Phase 3 failed: aggregate.awk crashed or returned non-zero exit code. Stderr: {e.stderr}")

    assert "StdDev:" in output, "Phase 3 failed: aggregate.awk output does not contain 'StdDev:'."

    # We expect the standard deviation to be approximately 0.00748331, but the build script checks for 0.007
    assert "0.007" in output, f"Phase 3 failed: aggregate.awk output '{output}' does not contain the correct computed standard deviation (expected ~0.007)."

def test_build_success_flag():
    assert os.path.isfile(BUILD_FLAG), f"Build failed: {BUILD_FLAG} is missing. Did you successfully run build.sh?"