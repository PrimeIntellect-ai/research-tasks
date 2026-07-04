# test_final_state.py

import os
import pytest

BUILD_ORDER_PATH = "/home/user/build_order.txt"
DECODER_PATH = "/home/user/pkg-mgr/decoder"

def test_build_order_exists_and_correct():
    assert os.path.isfile(BUILD_ORDER_PATH), f"File {BUILD_ORDER_PATH} was not created."

    with open(BUILD_ORDER_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_nodes = {"App", "LibA", "LibB", "Core", "Standalone"}
    actual_nodes = set(lines)

    assert actual_nodes == expected_nodes, (
        f"build_order.txt does not contain the exact expected nodes. "
        f"Expected {expected_nodes}, got {actual_nodes}"
    )

    # Check topological order constraints
    idx = {node: i for i, node in enumerate(lines)}

    assert idx["Core"] < idx["LibA"], "Core must be built before LibA"
    assert idx["Core"] < idx["LibB"], "Core must be built before LibB"
    assert idx["LibA"] < idx["App"], "LibA must be built before App"
    assert idx["LibB"] < idx["App"], "LibB must be built before App"

def test_decoder_compiled():
    assert os.path.isfile(DECODER_PATH), "decoder binary was not compiled."
    assert os.access(DECODER_PATH, os.X_OK), "decoder binary is not executable."