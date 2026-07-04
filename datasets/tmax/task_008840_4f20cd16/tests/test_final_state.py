# test_final_state.py

import os
import random

def test_final_loss_value():
    """
    Recomputes the expected final loss based on the problem description
    and checks if the student's output matches exactly.
    """
    # Recompute the expected loss using the exact procedure
    random.seed(42)
    num_nodes = 20
    edges = set()
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if random.random() < 0.3:
                edges.add((i, j, random.uniform(0.1, 5.0)))

    capacities = [random.uniform(1.0, 10.0) for _ in range(num_nodes)]
    target_capacities = [5.0 for _ in range(num_nodes)]

    # 50 epochs of gradient descent with learning rate 0.05
    for epoch in range(50):
        for i in range(num_nodes):
            grad = 2 * (capacities[i] - target_capacities[i])
            capacities[i] -= 0.05 * grad

    # Sorting edges to ensure deterministic reduction order
    sorted_edges = sorted(list(edges), key=lambda x: (x[0], x[1]))
    edge_loss = sum(w for u, v, w in sorted_edges)
    node_loss = sum((c - t)**2 for c, t in zip(capacities, target_capacities))

    expected_loss = edge_loss + node_loss
    expected_str = f"{expected_loss:.6f}"

    file_path = "/home/user/final_loss.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist. The task requires saving the final loss here."

    with open(file_path, "r") as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected final loss to be exactly '{expected_str}', but got '{actual_str}'."

def test_network_sim_updated():
    """
    Checks if the script /home/user/network_sim.py was reasonably updated to fix the bugs.
    """
    file_path = "/home/user/network_sim.py"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    # Check for sorting logic
    assert "sorted(" in content or ".sort(" in content, "The script does not appear to sort the edges to fix the determinism issue."

    # Check for gradient descent update logic
    assert "capacities" in content, "The script is missing references to capacities."