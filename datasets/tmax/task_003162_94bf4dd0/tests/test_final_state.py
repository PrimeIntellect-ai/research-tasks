# test_final_state.py

import os
import subprocess
import pytest

def test_files_exist():
    expected_files = [
        "/home/user/optimizer.c",
        "/home/user/verify_connectivity.exp",
        "/home/user/apply.sh",
    ]
    for path in expected_files:
        assert os.path.exists(path), f"Missing required file: {path}"

def test_apply_script_runs_and_generates_outputs():
    # Run the agent's pipeline
    apply_script = "/home/user/apply.sh"
    assert os.access(apply_script, os.X_OK), f"{apply_script} is not executable"

    result = subprocess.run(["bash", apply_script], capture_output=True, text=True)
    assert result.returncode == 0, f"apply.sh failed with return code {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Check generated files
    assert os.path.exists("/home/user/optimizer"), "Optimizer binary was not compiled."
    assert os.path.exists("/home/user/optimized_policies.txt"), "Optimized policies file was not generated."

def test_optimized_policies_metric_and_semantics():
    stats_file = "/home/user/traffic_stats.csv"
    base_policies = "/home/user/base_policies.txt"
    optimized_policies = "/home/user/optimized_policies.txt"
    oracle_bin = "/app/policy_oracle"

    assert os.path.exists(stats_file), f"Missing {stats_file}"
    assert os.path.exists(base_policies), f"Missing {base_policies}"
    assert os.path.exists(optimized_policies), f"Missing {optimized_policies}"
    assert os.path.exists(oracle_bin), f"Missing {oracle_bin}"

    queries = []
    freqs = []
    with open(stats_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            src, dst, freq = line.split(',')
            queries.append(f"query {src} {dst}\n")
            freqs.append(int(freq))

    query_str = "".join(queries)

    # Run baseline to get expected semantics
    p_base = subprocess.Popen([oracle_bin, base_policies], 
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out_base, _ = p_base.communicate(query_str)
    base_results = out_base.strip().split('\n')

    # Run optimized
    p_opt = subprocess.Popen([oracle_bin, optimized_policies], 
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out_opt, _ = p_opt.communicate(query_str)
    opt_results = out_opt.strip().split('\n')

    assert len(base_results) == len(opt_results) == len(freqs), "Oracle output length mismatch."

    total_weighted_latency = 0
    total_frequency = 0

    for i in range(len(freqs)):
        base_action = base_results[i].split()[0]
        opt_action = opt_results[i].split()[0]

        assert base_action == opt_action, f"Semantics changed for query {queries[i].strip()}! Expected {base_action}, got {opt_action}"

        latency_str = opt_results[i].split()[1]
        assert latency_str.endswith("ms"), f"Unexpected latency format: {latency_str}"
        latency = int(latency_str.replace('ms', ''))

        total_weighted_latency += latency * freqs[i]
        total_frequency += freqs[i]

    assert total_frequency > 0, "No traffic frequencies found."

    avg_latency = total_weighted_latency / total_frequency
    threshold = 12.5

    assert avg_latency <= threshold, f"FAILURE: Average latency {avg_latency:.2f} exceeds the threshold > {threshold}"