# test_final_state.py

import os
import pytest

def test_build_order_exists_and_valid():
    """Verify that build_order.txt exists and contains a valid topological sort."""
    build_order_file = "/home/user/project/build_order.txt"
    assert os.path.isfile(build_order_file), f"Expected file {build_order_file} does not exist."

    with open(build_order_file, "r") as f:
        content = f.read().strip()

    assert content, "build_order.txt is empty."

    # Parse the build order
    order = content.split()

    # Define the exact dependencies based on deps.txt
    # Format: target: [dependencies]
    deps = {
        "waf_core": ["http_parser", "rust_sanitizer"],
        "http_parser": ["utils", "logger"],
        "rust_sanitizer": ["utils"],
        "logger": ["utils"],
        "utils": []
    }

    # Ensure all nodes are present
    expected_nodes = set(deps.keys())
    actual_nodes = set(order)
    assert actual_nodes == expected_nodes, f"Build order must contain exactly {expected_nodes}, but found {actual_nodes}"

    # Check topological order constraints
    # A dependency must appear before the target that depends on it
    order_indices = {node: idx for idx, node in enumerate(order)}

    for target, dependencies in deps.items():
        for dep in dependencies:
            assert order_indices[dep] < order_indices[target], (
                f"Topological sort failed: dependency '{dep}' must appear before target '{target}'."
            )

def test_rust_sanitizer_compiled():
    """Verify that the Rust library was compiled in release mode successfully."""
    rlib_path = "/home/user/project/rust_sanitizer/target/release/librust_sanitizer.rlib"
    assert os.path.isfile(rlib_path), (
        f"Expected compiled Rust library at {rlib_path} does not exist. "
        "Ensure the borrow checker issue is fixed and the crate is built with --release."
    )