# test_final_state.py

import os
import re

def test_project_and_scripts_exist():
    """Verify that the Rust project directory and bash scripts exist."""
    assert os.path.isdir("/home/user/gbm_sim"), "Rust project directory /home/user/gbm_sim does not exist."
    assert os.path.isfile("/home/user/run_convergence.sh"), "Script /home/user/run_convergence.sh does not exist."
    assert os.path.isfile("/home/user/profile_parallel.sh"), "Script /home/user/profile_parallel.sh does not exist."

def test_convergence_log():
    """Verify the existence, format, and convergence logic of convergence.log."""
    log_path = "/home/user/convergence.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {log_path}, found {len(lines)}."

    expected_dts = ["0.1", "0.01", "0.001"]
    ks_distances = []

    for i, line in enumerate(lines):
        parts = line.split(",")
        assert len(parts) == 2, f"Line {i+1} in {log_path} is not in the format <dt>,<KS_distance>. Found: {line}"
        dt_str, ks_str = parts[0].strip(), parts[1].strip()

        assert dt_str == expected_dts[i], f"Expected dt={expected_dts[i]} on line {i+1}, found {dt_str}."

        try:
            ks_val = float(ks_str)
            ks_distances.append(ks_val)
        except ValueError:
            assert False, f"KS distance on line {i+1} is not a valid float: {ks_str}"

    # Check convergence logic: KS distance for dt=0.001 should be smaller than for dt=0.1
    ks_1 = ks_distances[0]
    ks_3 = ks_distances[2]
    assert ks_3 < ks_1, f"Convergence not demonstrated: KS distance for dt=0.001 ({ks_3}) is not smaller than for dt=0.1 ({ks_1})."

def test_profile_log():
    """Verify the existence, format, and speedup logic of profile.log."""
    log_path = "/home/user/profile.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}."

    thread_times = {}
    for i, line in enumerate(lines):
        # Expected format: threads=X,time=Y
        match = re.match(r"^threads=(\d+),time=([0-9]*\.?[0-9]+)$", line)
        assert match, f"Line {i+1} in {log_path} does not match expected format 'threads=X,time=Y'. Found: {line}"

        threads = int(match.group(1))
        time_val = float(match.group(2))
        thread_times[threads] = time_val

    assert 1 in thread_times, f"Missing 'threads=1' entry in {log_path}."
    assert 4 in thread_times, f"Missing 'threads=4' entry in {log_path}."

    t1 = thread_times[1]
    t4 = thread_times[4]

    # Check parallel speedup
    assert t4 < t1, f"Parallel speedup not demonstrated: time for threads=4 ({t4}) is not smaller than time for threads=1 ({t1})."