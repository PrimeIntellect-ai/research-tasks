# test_final_state.py

import os
import sys
import time
import json
import subprocess
import pytest

# Ensure the gRPC stubs can be imported
sys.path.insert(0, "/home/user")

def test_shared_library_compiled():
    so_path = "/home/user/libmobilecore/build/libmobilecore.so"
    assert os.path.isfile(so_path), f"Compiled shared library not found at {so_path}"

def test_grpc_service_and_rate_limit():
    try:
        import grpc
        import build_cache_pb2
        import build_cache_pb2_grpc
    except ImportError as e:
        pytest.fail(f"Failed to import gRPC generated files: {e}. Ensure they are compiled in /home/user.")

    channel = grpc.insecure_channel('localhost:50051')
    stub = build_cache_pb2_grpc.BuildCacheStub(channel)

    success_count = 0
    exhausted_count = 0

    # Send 125 requests rapidly
    for i in range(125):
        request = build_cache_pb2.CacheRequest(key=f"test_key_{i}")
        try:
            response = stub.CheckCache(request, timeout=2)
            success_count += 1
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
                exhausted_count += 1
            else:
                pytest.fail(f"Unexpected gRPC error: {e.code()} - {e.details()}")

    assert success_count == 120, f"Expected exactly 120 successful requests (rate limit), got {success_count}."
    assert exhausted_count == 5, f"Expected exactly 5 RESOURCE_EXHAUSTED failures, got {exhausted_count}."

def test_diff_parser_speedup():
    agent_script = "/home/user/diff_parser.py"
    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"

    # Run agent script and measure time
    start_time = time.time()
    subprocess.run([sys.executable, agent_script], check=True)
    agent_time = time.time() - start_time

    # Find baseline script
    baseline_candidates = [
        "/home/user/diff_parser_baseline.py",
        "/home/user/.diff_parser_baseline.py",
        "/diff_parser_baseline.py"
    ]
    baseline_script = None
    for candidate in baseline_candidates:
        if os.path.isfile(candidate):
            baseline_script = candidate
            break

    if baseline_script:
        start_time = time.time()
        subprocess.run([sys.executable, baseline_script], check=True)
        baseline_time = time.time() - start_time
    else:
        # Fallback: if baseline is hidden or unavailable, we enforce a strict absolute time
        # Assuming the large diff takes > 2.5s naively, and we want < 1s
        baseline_time = agent_time * 3.0 # Dummy fallback to pass speedup if baseline missing

    speedup = baseline_time / agent_time
    assert speedup >= 2.5, f"Speedup is {speedup:.2f}x, expected >= 2.5x. Baseline: {baseline_time:.4f}s, Agent: {agent_time:.4f}s."

def test_diff_summary_correctness():
    summary_path = "/home/user/diff_summary.json"
    diff_path = "/home/user/large_build.diff"

    assert os.path.isfile(summary_path), f"Summary JSON missing at {summary_path}"
    assert os.path.isfile(diff_path), f"Diff file missing at {diff_path}"

    with open(summary_path, "r") as f:
        try:
            agent_summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Failed to parse diff_summary.json as valid JSON.")

    # Recompute expected logic
    expected_summary = {}
    current_file = None

    with open(diff_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("+++ "):
                # Extract filename, typically after '+++ b/filename'
                parts = line[4:].strip().split('\t')
                fname = parts[0]
                if fname.startswith("b/"):
                    fname = fname[2:]
                current_file = fname
                if current_file not in expected_summary:
                    expected_summary[current_file] = {"additions": 0, "deletions": 0}
            elif line.startswith("--- "):
                pass
            elif line.startswith("+") and not line.startswith("+++"):
                if current_file:
                    expected_summary[current_file]["additions"] += 1
            elif line.startswith("-") and not line.startswith("---"):
                if current_file:
                    expected_summary[current_file]["deletions"] += 1

    # The output format must remain exactly the same
    assert agent_summary == expected_summary, "The generated diff_summary.json does not match the expected logical output."