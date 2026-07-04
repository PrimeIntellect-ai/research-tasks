# test_final_state.py

import os
import json
import subprocess
import pytest

def run_detector(corpus_dir):
    script_path = "/home/user/detector.py"
    assert os.path.isfile(script_path), f"Detector script not found at {script_path}"

    result = subprocess.run(
        ["python3", script_path, corpus_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Detector script failed with return code {result.returncode}.\nStderr: {result.stderr}"

    try:
        output_json = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Detector script did not output valid JSON.\nStdout: {result.stdout}")

    return output_json

def test_detector_evil_corpus():
    corpus_dir = "/var/opt/eval/evil/"
    assert os.path.isdir(corpus_dir), f"Evil corpus directory is missing at {corpus_dir}"

    expected_files = set(os.listdir(corpus_dir))
    output_json = run_detector(corpus_dir)

    bypassed = []
    for f in expected_files:
        if f not in output_json:
            bypassed.append(f"{f} (missing from output)")
        elif not output_json[f]:
            bypassed.append(f"{f} (flagged False, expected True)")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(expected_files)} evil bypassed:\n" + "\n".join(bypassed))

def test_detector_clean_corpus():
    corpus_dir = "/var/opt/eval/clean/"
    assert os.path.isdir(corpus_dir), f"Clean corpus directory is missing at {corpus_dir}"

    expected_files = set(os.listdir(corpus_dir))
    output_json = run_detector(corpus_dir)

    modified = []
    for f in expected_files:
        if f not in output_json:
            modified.append(f"{f} (missing from output)")
        elif output_json[f]:
            modified.append(f"{f} (flagged True, expected False)")

    if modified:
        pytest.fail(f"{len(modified)} of {len(expected_files)} clean modified (falsely flagged):\n" + "\n".join(modified))