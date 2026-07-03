# test_final_state.py

import os
import pytest

BUILD_ORDER_FILE = "/home/user/build_order.txt"
EXPECTED_ORDER = "alpha, beta, delta, gamma, epsilon"

def test_build_order_file_exists():
    assert os.path.isfile(BUILD_ORDER_FILE), f"The file {BUILD_ORDER_FILE} does not exist. Did you create it?"

def test_build_order_content():
    assert os.path.isfile(BUILD_ORDER_FILE), f"The file {BUILD_ORDER_FILE} does not exist."
    with open(BUILD_ORDER_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == EXPECTED_ORDER, (
        f"The build order is incorrect.\n"
        f"Expected: '{EXPECTED_ORDER}'\n"
        f"Got:      '{content}'"
    )