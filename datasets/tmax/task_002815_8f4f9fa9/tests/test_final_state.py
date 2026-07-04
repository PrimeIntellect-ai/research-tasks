# test_final_state.py
import os
import subprocess
import pytest

TASK_DIR = "/home/user/task"

def test_aggregate_sh_fixed():
    script_path = os.path.join(TASK_DIR, "aggregate.sh")
    assert os.path.isfile(script_path), "aggregate.sh is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # Check that it doesn't use the exact original non-deterministic find command
    original_cmd = 'find . -maxdepth 1 -name "partial_${N}_*.dat" | xargs awk'
    assert original_cmd not in content, "aggregate.sh still uses the non-deterministic `find ... | xargs awk` without sorting."

def test_results_and_log():
    log_file = os.path.join(TASK_DIR, "convergence.log")
    assert os.path.isfile(log_file), "convergence.log does not exist."

    with open(log_file, "r") as f:
        log_lines = [line.strip() for line in f if line.strip()]

    assert len(log_lines) == 4, f"convergence.log should have exactly 4 lines, but found {len(log_lines)}."

    expected_N_values = [2, 4, 8, 16]

    for idx, N in enumerate(expected_N_values):
        # 1. Recompute expected result using awk in strictly increasing numerical order
        files = [f"partial_{N}_{i}.dat" for i in range(1, N + 1)]
        files_paths = [os.path.join(TASK_DIR, f) for f in files]

        for fp in files_paths:
            assert os.path.isfile(fp), f"Expected partial file {fp} is missing."

        awk_cmd = ["awk", "{a[FNR]+=$1} END {for(i=1;i<=1000;i++) print a[i]}"] + files_paths
        result = subprocess.run(awk_cmd, capture_output=True, text=True, check=True)
        expected_result_text = result.stdout

        # Write to a temp file to use with compute_distance.py
        temp_result = os.path.join(TASK_DIR, f"temp_expected_result_{N}.dat")
        with open(temp_result, "w") as f:
            f.write(expected_result_text)

        # Run compute_distance.py to get the exact expected distance string
        dist_cmd = [
            "python3", 
            os.path.join(TASK_DIR, "compute_distance.py"), 
            temp_result, 
            os.path.join(TASK_DIR, "reference.dat")
        ]
        dist_result = subprocess.run(dist_cmd, capture_output=True, text=True, check=True)
        expected_distance = dist_result.stdout.strip()

        os.remove(temp_result)

        # 2. Check result_<N>.dat exists
        result_file = os.path.join(TASK_DIR, f"result_{N}.dat")
        assert os.path.isfile(result_file), f"result_{N}.dat does not exist."

        # 3. Check the log file contains the correctly formatted line
        expected_line = f"N={N} distance={expected_distance}"
        assert log_lines[idx] == expected_line, (
            f"Log line {idx+1} is incorrect.\n"
            f"Expected: '{expected_line}'\n"
            f"Got:      '{log_lines[idx]}'"
        )