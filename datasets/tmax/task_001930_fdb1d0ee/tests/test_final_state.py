# test_final_state.py
import os
import stat
import subprocess

def test_get_links_fixed():
    script_path = "/home/user/get_links.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    # Run the script and check output
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed to execute."

    lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    assert len(lines) == 6, f"Expected exactly 6 rows from the fixed query, but got {len(lines)}."

    # Check if the format is correct (source|dest|latency)
    for line in lines:
        parts = line.split('|')
        assert len(parts) == 3, f"Output line '{line}' is not in the expected format 'source|dest|latency'."
        assert parts[2].isdigit(), f"Latency '{parts[2]}' in line '{line}' is not a number."

def test_calc_shortest_path_exists_and_executable():
    script_path = "/home/user/calc_shortest_path.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_restore_plan_correct():
    plan_path = "/home/user/restore_plan.txt"
    assert os.path.exists(plan_path), f"File {plan_path} does not exist."

    with open(plan_path, "r") as f:
        content = f.read().strip()

    expected_content = "Path: backup-01 -> relay-01 -> relay-02 -> db-target-01 | Total Latency: 30"
    assert content == expected_content, f"File {plan_path} content is incorrect. Expected '{expected_content}', got '{content}'."