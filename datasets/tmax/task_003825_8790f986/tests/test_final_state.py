# test_final_state.py
import os

def test_solution_file():
    sol_path = "/home/user/solution.txt"
    exp_path = "/home/user/expected_solution.txt"

    assert os.path.exists(sol_path), f"Solution file {sol_path} does not exist."
    assert os.path.exists(exp_path), f"Expected solution file {exp_path} does not exist."

    with open(sol_path, "r") as f:
        sol_content = f.read().strip()

    with open(exp_path, "r") as f:
        exp_content = f.read().strip()

    assert sol_content == exp_content, f"Expected variance {exp_content}, but got {sol_content} in {sol_path}."

def test_memory_leak_fixed():
    script_path = "/home/user/service/packet_processor.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "self.history.append" not in content, "Memory leak still present: self.history.append is still in packet_processor.py"