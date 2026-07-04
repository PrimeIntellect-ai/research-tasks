# test_final_state.py

import os
import subprocess
import time
import pytest

def run_and_time(cmd):
    start = time.time()
    res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
    duration = time.time() - start
    return res.stdout, duration

def test_fast_search_speedup_and_accuracy():
    fast_search = "/home/user/fast_search"
    ref_search = "/app/ref_search"
    dataset = "/home/user/dataset.bin"
    queries = "/home/user/queries.bin"

    assert os.path.exists(fast_search), f"fast_search binary not found at {fast_search}"
    assert os.access(fast_search, os.X_OK), f"fast_search at {fast_search} is not executable"

    ref_out, ref_time = run_and_time([ref_search, dataset, queries])
    fast_out, fast_time = run_and_time([fast_search, dataset, queries])

    assert ref_out.strip() == fast_out.strip(), "Output of fast_search does not match ref_search exactly."

    speedup = ref_time / fast_time
    assert speedup >= 5.0, f"Speedup {speedup:.2f} is less than the required threshold of 5.0."

def test_benchmark_script_and_ci_txt():
    benchmark_script = "/home/user/benchmark.py"
    ci_txt = "/home/user/ci.txt"

    assert os.path.exists(benchmark_script), f"benchmark.py not found at {benchmark_script}"
    assert os.path.exists(ci_txt), f"ci.txt not found at {ci_txt}"

    with open(ci_txt, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 2, f"ci.txt must contain exactly two comma-separated floats. Found: {content}"

    try:
        lower = float(parts[0].strip())
        upper = float(parts[1].strip())
    except ValueError:
        pytest.fail(f"ci.txt contents are not valid floats. Found: {content}")

    assert lower <= upper, f"Lower bound ({lower}) of CI must be less than or equal to upper bound ({upper})."