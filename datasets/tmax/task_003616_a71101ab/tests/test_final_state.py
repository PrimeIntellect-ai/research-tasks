# test_final_state.py

import os
import csv
import math
import subprocess
import pytest

def test_dependencies_installed():
    """Test that g++ and boost-math-dev are installed."""
    # Check if g++ is installed
    try:
        subprocess.run(['g++', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.fail("g++ is not installed or not in PATH.")

    # Check if boost math distributions header exists
    boost_header = '/usr/include/boost/math/distributions/beta.hpp'
    assert os.path.isfile(boost_header), f"Boost math header {boost_header} not found. libboost-math-dev might not be installed."

def test_bug_fixed_in_source():
    """Test that the integer division bug was removed from the source code."""
    source_file = '/home/user/tracker/artifact_tracker.cpp'
    assert os.path.isfile(source_file), f"Source file {source_file} is missing."

    with open(source_file, 'r') as f:
        content = f.read()

    # The original buggy line
    buggy_snippet = "(int(p_alpha) - 1) / (int(p_alpha) + int(p_beta) - 2)"
    assert buggy_snippet not in content, "The integer division bug is still present in artifact_tracker.cpp."

def test_binary_compiled():
    """Test that the artifact_tracker binary exists and is executable."""
    binary_path = '/home/user/tracker/artifact_tracker'
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def compute_expected_results():
    """Helper to compute the expected results from the input files."""
    models = {}

    with open('/home/user/data/models.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            models[row['model_id']] = {
                'prior_alpha': float(row['prior_alpha']),
                'prior_beta': float(row['prior_beta'])
            }

    with open('/home/user/data/trials.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            m_id = row['model_id']
            models[m_id]['successes'] = int(row['successes'])
            models[m_id]['failures'] = int(row['failures'])
            models[m_id]['embedding'] = [float(x) for x in row['embedding'].split(';')]

    with open('/home/user/data/query.txt', 'r') as f:
        query_str = f.read().strip()
        query = [float(x) for x in query_str.split(';')]

    results = {}
    for m_id, data in models.items():
        p_alpha = data['prior_alpha'] + data['successes']
        p_beta = data['prior_beta'] + data['failures']

        map_est = (p_alpha - 1.0) / (p_alpha + p_beta - 2.0)

        emb = data['embedding']
        dot = sum(a * b for a, b in zip(emb, query))
        norm_emb = math.sqrt(sum(a * a for a in emb))
        norm_q = math.sqrt(sum(a * a for a in query))
        sim = dot / (norm_emb * norm_q)

        final_score = map_est * sim

        results[m_id] = {
            'post_alpha': p_alpha,
            'post_beta': p_beta,
            'map_estimate': map_est,
            'similarity': sim,
            'final_score': final_score
        }

    return results

def test_output_csv_correctness():
    """Test that output.csv is generated and contains the correctly computed values."""
    output_file = '/home/user/tracker/output.csv'
    assert os.path.isfile(output_file), f"Output file {output_file} was not generated."

    expected = compute_expected_results()

    actual = {}
    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            actual[row['model_id']] = {
                'post_alpha': float(row['post_alpha']),
                'post_beta': float(row['post_beta']),
                'map_estimate': float(row['map_estimate']),
                'similarity': float(row['similarity']),
                'final_score': float(row['final_score'])
            }

    assert len(actual) == len(expected), "Output CSV does not have the expected number of models."

    tolerance = 0.001
    for m_id, exp_vals in expected.items():
        assert m_id in actual, f"Model {m_id} missing from output."
        act_vals = actual[m_id]

        for key in ['post_alpha', 'post_beta', 'map_estimate', 'similarity', 'final_score']:
            diff = abs(exp_vals[key] - act_vals[key])
            assert diff <= tolerance, (
                f"Value mismatch for model {m_id}, metric {key}: "
                f"Expected ~{exp_vals[key]:.4f}, got {act_vals[key]:.4f}"
            )