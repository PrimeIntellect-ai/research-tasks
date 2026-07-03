# test_final_state.py
import os
import re
import subprocess
import time
import pytest

def test_math_utils_fixed():
    path = "/home/user/legacy_project/math_utils.c"
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, "r") as f:
        content = f.read()

    # The bitwise XOR operator ^ should be removed from the calculation
    assert "^" not in content, "math_utils.c still contains the bitwise XOR operator '^'"
    # It should use * or pow for squaring
    assert "*" in content or "pow" in content, "math_utils.c does not seem to use multiplication or pow() for squaring"

def test_processor_bottleneck_fixed():
    path = "/home/user/legacy_project/processor.c"
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, "r") as f:
        content = f.read()

    # The usleep should be removed to fix the bottleneck
    assert "usleep" not in content, "processor.c still contains the usleep() bottleneck"

def test_processor_compiles_and_runs_fast():
    # Compile the processor
    compile_cmd = ["gcc", "-o", "processor", "processor.c", "math_utils.c", "-lm"]
    result = subprocess.run(compile_cmd, cwd="/home/user/legacy_project", capture_output=True)
    assert result.returncode == 0, f"Compilation failed: {result.stderr.decode()}"

    # Run the processor and measure time
    start_time = time.time()
    run_cmd = ["./processor"]
    result = subprocess.run(run_cmd, cwd="/home/user/legacy_project", capture_output=True)
    end_time = time.time()

    assert result.returncode == 0, "Processor execution failed"

    elapsed = end_time - start_time
    assert elapsed < 0.5, f"Processor is still too slow, took {elapsed:.2f} seconds (expected < 0.1s)"

def test_mre_bottleneck_exists():
    path = "/home/user/mre_bottleneck.c"
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, "r") as f:
        content = f.read()

    assert "fsync" in content, "mre_bottleneck.c does not contain fsync()"
    assert "usleep" in content, "mre_bottleneck.c does not contain usleep()"
    assert "while" in content or "for" in content, "mre_bottleneck.c should contain a loop demonstrating the bottleneck"

def test_reconstruct_logs_script():
    script_path = "/home/user/reconstruct_logs.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing"

    # Ensure it's executable or run it with bash
    result = subprocess.run(["bash", script_path], capture_output=True)
    assert result.returncode == 0, f"reconstruct_logs.sh failed to execute: {result.stderr.decode()}"

    timeline_path = "/home/user/timeline.log"
    assert os.path.isfile(timeline_path), f"{timeline_path} was not generated"

    with open(timeline_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "timeline.log is empty"

    previous_time = 0.0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Expected format: [<EPOCH_TIME>] <COMPONENT> : <MESSAGE>
        match = re.match(r'^\[(\d+(?:\.\d+)?)\]\s+(GEN|PROC|AGG)\s+:\s+(.*)$', line)
        assert match is not None, f"Line format is incorrect: {line}"

        current_time = float(match.group(1))
        assert current_time >= previous_time, "timeline.log is not chronologically sorted"
        previous_time = current_time