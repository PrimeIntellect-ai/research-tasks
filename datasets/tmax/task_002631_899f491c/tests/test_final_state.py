# test_final_state.py

import os
import json
import subprocess
import pytest

def test_settings_json_exists_and_valid():
    settings_path = "/home/user/app/settings.json"
    assert os.path.isfile(settings_path), f"The file {settings_path} must exist."

    with open(settings_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{settings_path} does not contain valid JSON.")

    assert data == {}, f"{settings_path} should contain an empty JSON object {{}}."

def test_mre_py_exists_and_incorrect_variance():
    mre_path = "/home/user/mre.py"
    assert os.path.isfile(mre_path), f"The file {mre_path} must exist."

    with open(mre_path, "r") as f:
        content = f.read()

    assert "1000000001.0" in content and "1000000002.0" in content and "1000000003.0" in content, \
        f"{mre_path} must contain the hardcoded list of numbers."

    # Run the MRE script and check its output
    result = subprocess.run(["python3", mre_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {mre_path} failed with error: {result.stderr}"

    output = result.stdout.strip()
    try:
        calculated_variance = float(output)
    except ValueError:
        pytest.fail(f"Output of {mre_path} could not be parsed as a float. Output was: {output}")

    # The true variance of [1000000001.0, 1000000002.0, 1000000003.0] is 1.0
    # The naive formula will produce 0.0 or something completely off due to precision loss.
    assert calculated_variance != 1.0, f"{mre_path} is supposed to demonstrate the buggy naive formula, but it produced the correct variance (1.0)."

def test_processor_py_fixed():
    processor_path = "/home/user/app/processor.py"
    assert os.path.isfile(processor_path), f"The file {processor_path} must exist."

    # Run the processor script to ensure it doesn't crash and works correctly
    result = subprocess.run(["python3", processor_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {processor_path} failed with error: {result.stderr}"

    output = result.stdout.strip()
    try:
        calculated_variance = float(output)
    except ValueError:
        pytest.fail(f"Output of {processor_path} could not be parsed as a float. Output was: {output}")

    assert abs(calculated_variance - 2.5) < 1e-5, f"The variance calculated by {processor_path} is incorrect. Expected 2.5, got {calculated_variance}."

def test_variance_output_txt_exists_and_correct():
    output_path = "/home/user/variance_output.txt"
    assert os.path.isfile(output_path), f"The file {output_path} must exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    try:
        saved_variance = float(content)
    except ValueError:
        pytest.fail(f"Content of {output_path} could not be parsed as a float. Content was: {content}")

    assert abs(saved_variance - 2.5) < 1e-5, f"The variance saved in {output_path} is incorrect. Expected 2.5, got {saved_variance}."