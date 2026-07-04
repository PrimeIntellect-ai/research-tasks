# test_final_state.py

import os
import json
import math
import subprocess
import pytest

def calculate_ground_truth(fasta_path):
    group_a = []
    group_b = []

    with open(fasta_path, 'r') as f:
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq:
                    gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
                    if 'ATGCATGC' in seq:
                        group_a.append(gc)
                    else:
                        group_b.append(gc)
                seq = ""
            else:
                seq += line
        if seq:
            gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
            if 'ATGCATGC' in seq:
                group_a.append(gc)
            else:
                group_b.append(gc)

    mean_a = sum(group_a) / len(group_a) if group_a else 0.0
    mean_b = sum(group_b) / len(group_b) if group_b else 0.0
    diff = abs(mean_a - mean_b)
    significant = diff > 5.0

    return {
        "group_a_mean": mean_a,
        "group_b_mean": mean_b,
        "difference": diff,
        "significant": significant,
        "num_group_a": len(group_a),
        "num_group_b": len(group_b)
    }

def test_results_json():
    results_path = '/home/user/analysis/results.json'
    assert os.path.isfile(results_path), f"Missing {results_path}"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON")

    fasta_path = '/home/user/data/input.fasta'
    truth = calculate_ground_truth(fasta_path)

    assert results.get("num_group_a") == truth["num_group_a"], "Incorrect count for Group A"
    assert results.get("num_group_b") == truth["num_group_b"], "Incorrect count for Group B"
    assert results.get("significant") == truth["significant"], "Incorrect significance boolean"

    assert math.isclose(results.get("group_a_mean", 0), truth["group_a_mean"], abs_tol=0.005), "Incorrect Group A mean"
    assert math.isclose(results.get("group_b_mean", 0), truth["group_b_mean"], abs_tol=0.005), "Incorrect Group B mean"
    assert math.isclose(results.get("difference", 0), truth["difference"], abs_tol=0.005), "Incorrect difference"

def test_plot_exists():
    plot_path = '/home/user/analysis/gc_plot.png'
    assert os.path.isfile(plot_path), f"Missing {plot_path}"
    with open(plot_path, 'rb') as f:
        header = f.read(8)
        assert header == b'\x89PNG\r\n\x1a\n', f"File {plot_path} is not a valid PNG image"

def test_go_test_passes():
    test_file = '/home/user/analysis/analyzer_test.go'
    assert os.path.isfile(test_file), f"Missing {test_file}"

    with open(test_file, 'r') as f:
        content = f.read()
        assert "func Test" in content, f"No tests found in {test_file}"

    result = subprocess.run(['go', 'test'], cwd='/home/user/analysis', capture_output=True, text=True)
    assert result.returncode == 0, f"go test failed:\n{result.stdout}\n{result.stderr}"

def test_concurrency_used():
    main_file = '/home/user/analysis/main.go'
    assert os.path.isfile(main_file), f"Missing {main_file}"

    with open(main_file, 'r') as f:
        content = f.read()
        has_go = "go " in content
        has_chan = "chan " in content
        has_wg = "WaitGroup" in content

        assert has_go and (has_chan or has_wg), "Concurrency primitives (goroutines and channels/WaitGroups) not found in main.go"