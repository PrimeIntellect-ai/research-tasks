# test_final_state.py
import os
import sys
import json
import subprocess
import pytest

def test_detector_results():
    detector_path = "/app/detector.py"
    input_dir = "/app/corpora/eval_mixed"
    output_json = "/tmp/results.json"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isfile(detector_path), f"Detector script not found at {detector_path}"

    # Ensure the output file does not exist before running
    if os.path.exists(output_json):
        os.remove(output_json)

    # Run the detector
    try:
        subprocess.run(
            [sys.executable, detector_path, input_dir, output_json],
            check=True,
            capture_output=True,
            text=True,
            timeout=30
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Detector script failed with exit code {e.returncode}.\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Detector script timed out after 30 seconds.")

    assert os.path.isfile(output_json), f"Output JSON not found at {output_json}"

    with open(output_json, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_json} is not valid JSON.")

    assert isinstance(results, dict), f"Expected JSON output to be a dictionary, got {type(results).__name__}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.wav')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.wav')]

    bypassed_evil = []
    modified_clean = []

    for f in evil_files:
        if results.get(f) != "REJECT":
            bypassed_evil.append(f)

    for f in clean_files:
        if results.get(f) != "ACCEPT":
            modified_clean.append(f)

    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))