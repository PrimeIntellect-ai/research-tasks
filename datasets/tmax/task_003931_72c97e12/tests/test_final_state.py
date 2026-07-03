# test_final_state.py

import os

def test_fixed_output_log_exists_and_correct():
    log_file = "/home/user/fixed_output.log"
    assert os.path.exists(log_file), f"{log_file} does not exist. Did you run the script and change the output path?"
    assert os.path.isfile(log_file), f"{log_file} should be a file."

    with open(log_file, "r") as f:
        content = f.read().strip()

    assert content, f"{log_file} is empty."

    lines = content.split('\n')
    assert len(lines) == 10, f"Log file should contain exactly 10 lines, found {len(lines)}."

    expected_lines = {f"Line_data_from_worker_{i}" for i in range(10)}
    actual_lines = set(lines)

    assert actual_lines == expected_lines, "Log file contains garbled or missing lines due to race condition. Ensure the environment variable is passed correctly."

def test_aggregator_script_modifications():
    script_path = "/home/user/aggregator.py"
    assert os.path.exists(script_path), f"{script_path} does not exist."

    with open(script_path, "r") as f:
        script_content = f.read()

    assert "fixed_output.log" in script_content, "The script does not seem to target 'fixed_output.log'."
    assert "FORCE_SAFE_LOGGING_99" in script_content, "The script does not seem to contain the correct environment variable 'FORCE_SAFE_LOGGING_99'."