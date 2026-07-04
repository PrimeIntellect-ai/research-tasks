# test_final_state.py
import os

def test_final_output_exists_and_correct():
    output_path = "/home/user/project/final_output.txt"
    assert os.path.isfile(output_path), f"{output_path} is missing."

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "14.9927", f"Expected final output to be exactly '14.9927', but got '{content}'."

def test_trace_log_exists_and_correct():
    trace_path = "/home/user/project/trace.log"
    assert os.path.isfile(trace_path), f"{trace_path} is missing."

    with open(trace_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Iteration 1: 7.5000",
        "Iteration 2: 11.2500",
        "Iteration 3: 13.1250",
        "Iteration 4: 14.0625",
        "Iteration 5: 14.5312",
        "Iteration 6: 14.7656",
        "Iteration 7: 14.8828",
        "Iteration 8: 14.9414",
        "Iteration 9: 14.9707",
        "Iteration 10: 14.9854",
        "Iteration 11: 14.9927"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} trace lines, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}: expected '{expected}', got '{actual}'."

def test_script_is_executable():
    script_path = "/home/user/project/build_model.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."