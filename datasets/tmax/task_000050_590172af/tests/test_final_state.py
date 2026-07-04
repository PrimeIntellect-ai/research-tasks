# test_final_state.py
import os
import math

def test_fixed_script_exists():
    path = "/home/user/fixed_aggregate.py"
    assert os.path.isfile(path), f"The fixed script {path} does not exist."

def test_stable_result_exists():
    path = "/home/user/stable_result.txt"
    assert os.path.isfile(path), f"The result file {path} does not exist."

def test_stable_result_value():
    import h5py
    import numpy as np
    import networkx as nx

    data_path = "/home/user/data.h5"
    assert os.path.isfile(data_path), f"Data file {data_path} is missing."

    # Compute the expected deterministic truth
    with h5py.File(data_path, 'r') as f:
        signals = f['signals'][:]
        edges = f['edges'][:]

    G = nx.Graph()
    G.add_edges_from(edges)
    largest_cc = max(nx.connected_components(G), key=len)

    # Sort nodes to guarantee deterministic order
    sorted_nodes = sorted(list(largest_cc))
    cc_signals = [signals[i] for i in sorted_nodes]

    total_power = 0.0
    for sig in cc_signals:
        fft_vals = np.fft.rfft(sig)
        power = float(np.max(np.abs(fft_vals)))
        total_power += power

    expected_value = total_power

    result_path = "/home/user/stable_result.txt"
    with open(result_path, "r") as f:
        content = f.read().strip()

    try:
        student_value = float(content)
    except ValueError:
        assert False, f"The file {result_path} does not contain a valid float. Content: '{content}'"

    # Check if the student's value matches the expected deterministic value closely
    assert math.isclose(student_value, expected_value, rel_tol=1e-11), \
        f"The computed value {student_value} does not match the expected deterministic value {expected_value}."