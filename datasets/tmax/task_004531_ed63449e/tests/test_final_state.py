# test_final_state.py
import os
import math

def test_entropy_result():
    result_file = "/home/user/entropy_result.txt"
    assert os.path.exists(result_file), f"Result file is missing at {result_file}"
    assert os.path.isfile(result_file), f"Path {result_file} is not a file"

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content, f"File {result_file} is empty"

    try:
        agent_val = float(content)
    except ValueError:
        assert False, f"Content of {result_file} is not a valid float: {content}"

    target = 0.937636
    error = abs(agent_val - target)

    assert error <= 0.05, f"Metric threshold failed: error {error} > 0.05. Agent value: {agent_val}, Target: {target}"