# test_final_state.py
import os
import json
import math

def test_features_json_correctness():
    features_path = "/home/user/features.json"
    assert os.path.isfile(features_path), f"Output file {features_path} does not exist."

    with open(features_path, "r") as f:
        try:
            features = json.load(f)
        except json.JSONDecodeError:
            assert False, "features.json is not a valid JSON file."

    # Parse the PDB file to compute ground truth
    pdb_path = "/home/user/data/protein.pdb"
    assert os.path.isfile(pdb_path), "Original PDB file is missing."

    coords = []
    with open(pdb_path, "r") as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append((x, y, z))

    num_nodes = len(coords)
    num_edges = 0
    degrees = [0] * num_nodes

    # Compute edges and degrees
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            dist = math.sqrt(
                (coords[i][0] - coords[j][0])**2 +
                (coords[i][1] - coords[j][1])**2 +
                (coords[i][2] - coords[j][2])**2
            )
            if dist <= 8.0:
                num_edges += 1
                degrees[i] += 1
                degrees[j] += 1

    mean_degree = sum(degrees) / num_nodes if num_nodes > 0 else 0.0

    # Validate exact counts and computed metrics
    assert "num_nodes" in features, "Missing 'num_nodes' in JSON."
    assert features["num_nodes"] == num_nodes, f"Expected {num_nodes} nodes, got {features['num_nodes']}."

    assert "num_edges" in features, "Missing 'num_edges' in JSON."
    assert features["num_edges"] == num_edges, f"Expected {num_edges} edges, got {features['num_edges']}."

    assert "mean_degree" in features, "Missing 'mean_degree' in JSON."
    assert abs(features["mean_degree"] - mean_degree) < 1e-3, \
        f"Expected mean_degree approx {mean_degree:.4f}, got {features['mean_degree']}."

    # Validate bootstrap confidence intervals (structure and invariants)
    assert "ci_lower" in features, "Missing 'ci_lower' in JSON."
    assert "ci_upper" in features, "Missing 'ci_upper' in JSON."

    ci_lower = features["ci_lower"]
    ci_upper = features["ci_upper"]
    assert isinstance(ci_lower, float) or isinstance(ci_lower, int), "ci_lower must be a number."
    assert isinstance(ci_upper, float) or isinstance(ci_upper, int), "ci_upper must be a number."
    assert ci_lower <= features["mean_degree"] <= ci_upper, \
        "mean_degree should fall within the confidence interval [ci_lower, ci_upper]."

    # Validate MCMC nodes (structure and invariants)
    assert "top_5_mcmc_nodes" in features, "Missing 'top_5_mcmc_nodes' in JSON."
    top_5 = features["top_5_mcmc_nodes"]
    assert isinstance(top_5, list), "'top_5_mcmc_nodes' must be a list."
    assert len(top_5) == 5, f"Expected exactly 5 nodes in top_5_mcmc_nodes, got {len(top_5)}."

    for node in top_5:
        assert isinstance(node, int), f"Node index {node} is not an integer."
        assert 0 <= node < num_nodes, f"Node index {node} is out of bounds for the graph."