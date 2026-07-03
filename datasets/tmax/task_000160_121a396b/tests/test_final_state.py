# test_final_state.py

import os
import sqlite3
import subprocess
import time
import pytest

def get_db_configs():
    conn = sqlite3.connect("/data/configs.db")
    c = conn.cursor()
    c.execute("SELECT id, content FROM snapshots ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows

def parse_config(content):
    cfg = {}
    for line in content.strip().split('\n'):
        if '=' in line:
            k, v = line.split('=', 1)
            cfg[k] = v
    return cfg

def is_sensitive(key):
    k = key.lower()
    return 'secret' in k or 'password' in k or 'token' in k

def compute_diff(cfg1, cfg2):
    added = 0
    removed = 0
    modified = 0
    secrets_masked = 0

    keys1 = set(cfg1.keys())
    keys2 = set(cfg2.keys())

    for k in keys2 - keys1:
        if is_sensitive(k):
            secrets_masked += 1
        else:
            added += 1

    for k in keys1 - keys2:
        if is_sensitive(k):
            secrets_masked += 1
        else:
            removed += 1

    for k in keys1 & keys2:
        if cfg1[k] != cfg2[k]:
            if is_sensitive(k):
                secrets_masked += 1
            else:
                modified += 1

    return added, removed, modified, secrets_masked

def test_pipeline_artifacts():
    assert os.path.exists("/home/user/pipeline.sh"), "pipeline.sh missing"
    assert os.path.exists("/home/user/pipeline.log"), "pipeline.log missing"
    assert os.path.exists("/home/user/fast_tracker.c"), "fast_tracker.c missing"
    assert os.path.exists("/home/user/fast_tracker"), "fast_tracker binary missing"
    assert os.path.exists("/home/user/summary_stats.log"), "summary_stats.log missing"

def test_summary_stats_correctness():
    rows = get_db_configs()
    expected_lines = []
    total_a = total_r = total_m = total_s = 0

    for i in range(len(rows) - 1):
        id1, c1 = rows[i]
        id2, c2 = rows[i+1]
        cfg1 = parse_config(c1)
        cfg2 = parse_config(c2)

        a, r, m, s = compute_diff(cfg1, cfg2)
        total_a += a
        total_r += r
        total_m += m
        total_s += s

        expected_lines.append(f"{id1}.txt -> {id2}.txt: added: {a}, removed: {r}, modified: {m}, secrets_masked: {s}")

    expected_lines.append(f"TOTAL: added: {total_a}, removed: {total_r}, modified: {total_m}, secrets_masked: {total_s}")
    expected_output = "\n".join(expected_lines) + "\n"

    with open("/home/user/summary_stats.log", "r") as f:
        agent_output = f.read()

    assert agent_output.strip() == expected_output.strip(), "summary_stats.log content does not match expected output exactly."

def test_speedup_metric():
    # Baseline: calling oracle in a loop via subprocess
    # We simulate the baseline time by measuring the overhead of subprocess calls.
    configs_dir = "/home/user/configs"
    assert os.path.exists(configs_dir), "configs directory missing"

    files = sorted([f for f in os.listdir(configs_dir) if f.endswith('.txt')], key=lambda x: int(x.split('.')[0]))
    assert len(files) == 2000, "Expected 2000 config files extracted"

    start_baseline = time.time()
    for i in range(min(100, len(files) - 1)):
        f1 = os.path.join(configs_dir, files[i])
        f2 = os.path.join(configs_dir, files[i+1])
        subprocess.run(["/app/config_diff_oracle", f1, f2], stdout=subprocess.DEVNULL)
    end_baseline = time.time()

    # Extrapolate baseline time for all 1999 pairs
    baseline_time = (end_baseline - start_baseline) * (1999 / 100.0)

    start_agent = time.time()
    subprocess.run(["/home/user/fast_tracker", configs_dir], stdout=subprocess.DEVNULL)
    agent_time = time.time() - start_agent

    speedup = baseline_time / agent_time if agent_time > 0 else float('inf')
    assert speedup >= 10.0, f"Speedup metric failed: measured speedup is {speedup:.2f}x, threshold is 10.0x"