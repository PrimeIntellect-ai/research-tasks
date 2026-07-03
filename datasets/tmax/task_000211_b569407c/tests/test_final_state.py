# test_final_state.py
import os
import subprocess
import time
import pytest

def test_rust_exploit_speedup_and_correctness():
    cargo_dir = '/home/user/fast_exploit'
    assert os.path.isdir(cargo_dir), f"Rust project directory missing at {cargo_dir}."

    # Compile the agent's Rust project
    compile_proc = subprocess.run(
        ['cargo', 'build', '--release'], 
        cwd=cargo_dir, 
        capture_output=True, 
        text=True
    )
    assert compile_proc.returncode == 0, f"Cargo build failed:\n{compile_proc.stderr}\n{compile_proc.stdout}"

    bin_path = os.path.join(cargo_dir, 'target/release/fast_exploit')
    assert os.path.isfile(bin_path), f"Compiled binary not found at {bin_path}"

    # Measure baseline execution time and get the expected output
    baseline_times = []
    expected_output = ""
    for _ in range(5):
        start = time.perf_counter()
        proc = subprocess.run(['python3', '/app/baseline.py'], capture_output=True, text=True)
        baseline_times.append(time.perf_counter() - start)
        assert proc.returncode == 0, f"Baseline script failed:\n{proc.stderr}"
        expected_output = proc.stdout.strip()

    avg_baseline = sum(baseline_times) / len(baseline_times)

    # Measure agent execution time and get the agent output
    agent_times = []
    agent_output = ""
    for _ in range(5):
        start = time.perf_counter()
        proc = subprocess.run([bin_path], capture_output=True, text=True)
        agent_times.append(time.perf_counter() - start)
        assert proc.returncode == 0, f"Agent binary failed:\n{proc.stderr}"
        agent_output = proc.stdout.strip()

    avg_agent = sum(agent_times) / len(agent_times)

    # Check correctness
    assert agent_output == expected_output, (
        f"Agent output did not match expected checksum.\n"
        f"Expected: '{expected_output}'\n"
        f"Got: '{agent_output}'"
    )

    # Check performance metric
    speedup = avg_baseline / avg_agent
    assert speedup >= 3.0, (
        f"Performance requirement not met. "
        f"Baseline avg: {avg_baseline:.4f}s, Agent avg: {avg_agent:.4f}s. "
        f"Speedup is {speedup:.2f}x, which is less than the required 3.0x threshold."
    )