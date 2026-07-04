# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_json_sh_fix():
    json_sh_path = "/app/vendored/JSON.sh-0.4.1/JSON.sh"
    assert os.path.exists(json_sh_path), f"File missing: {json_sh_path}"

    # Run the JSON.sh script with a test payload containing hex unicode escapes
    payload = '{"test":"\\uabcd"}'
    result = subprocess.run(
        [json_sh_path, "-b"],
        input=payload,
        text=True,
        capture_output=True
    )

    assert result.returncode == 0, f"JSON.sh failed to execute. stderr: {result.stderr}"

    # Expected output structure from JSON.sh -b
    expected_output_fragment = '["test"]\t"\\uabcd"'
    assert expected_output_fragment in result.stdout, (
        f"JSON.sh did not correctly parse the hex unicode escape. "
        f"Expected to find '{expected_output_fragment}' in output, got:\n{result.stdout}"
    )

def test_anomaly_detector_corpus():
    detector_script = "/home/user/detect_anomalies.sh"
    assert os.path.exists(detector_script), f"Detector script missing: {detector_script}"
    assert os.access(detector_script, os.X_OK), f"Detector script is not executable: {detector_script}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for fpath in clean_files:
        result = subprocess.run([detector_script, fpath], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(fpath))

    evil_failed = []
    for fpath in evil_files:
        result = subprocess.run([detector_script, fpath], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(fpath))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    assert not error_messages, "Corpus verification failed:\n" + "\n".join(error_messages)