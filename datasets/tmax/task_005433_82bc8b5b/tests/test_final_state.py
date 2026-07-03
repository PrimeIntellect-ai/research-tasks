# test_final_state.py
import os
import pytest

def test_rust_library_compiled():
    """Verify that the Rust library was successfully compiled in release mode."""
    so_path = "/home/user/utility/rust_lib/target/release/librust_lib.so"
    assert os.path.isfile(so_path), (
        f"Compiled Rust library not found at {so_path}. "
        "Did you fix the borrow checker error and run 'cargo build --release'?"
    )

def test_load_order_correct():
    """Verify that resolver.py generated the correct topological sort output."""
    load_order_path = "/home/user/utility/load_order.txt"
    assert os.path.isfile(load_order_path), (
        f"Output file not found at {load_order_path}. "
        "Did you complete and run resolver.py?"
    )

    with open(load_order_path, "r") as f:
        content = f.read().strip()

    expected = "libdelta, libbeta, libgamma, libalpha, librust_lib"
    assert content == expected, (
        f"Incorrect load order in {load_order_path}.\n"
        f"Expected: {expected}\n"
        f"Got:      {content}\n"
        "Ensure you are breaking ties alphabetically and sorting dependencies before dependents."
    )