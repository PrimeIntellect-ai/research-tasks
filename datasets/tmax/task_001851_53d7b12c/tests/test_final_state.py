# test_final_state.py
import os
import pytest

def test_solution_correctness():
    log_path = "/home/user/data/perf.log"
    assert os.path.exists(log_path), f"File {log_path} is missing."

    # Principled computation of the expected average based on the log file
    total_score = 0.0
    count = 0

    with open(log_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            # The task specifies to safely ignore lines that do not have exactly 4 fields
            if len(parts) == 4:
                try:
                    cpu = float(parts[2])
                    mem = float(parts[3])
                    # Score = 50% CPU, 10% Memory
                    score = cpu * 0.5 + mem * 0.1
                    total_score += score
                    count += 1
                except ValueError:
                    pass

    assert count > 0, "No valid lines found in perf.log to compute average."
    expected_avg = total_score / count
    expected_str = f"{expected_avg:.2f}"

    sol_path = "/home/user/solution.txt"
    assert os.path.exists(sol_path), f"File {sol_path} is missing. Did you save the output?"

    with open(sol_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_str, (
        f"Incorrect average score in {sol_path}. "
        f"Expected '{expected_str}', but got '{actual_content}'."
    )

def test_go_mod_fixed():
    go_mod_path = "/home/user/perf-tool/go.mod"
    assert os.path.exists(go_mod_path), f"File {go_mod_path} is missing."

    with open(go_mod_path, "r") as f:
        content = f.read()

    assert "v1.9.9" not in content, "The go.mod file still contains the intentionally invalid version v1.9.9."