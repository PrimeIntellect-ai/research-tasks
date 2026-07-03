# test_final_state.py
import os
import json
import pytest

def test_build_order_valid():
    deps_path = "/home/user/project/deps.json"
    build_order_path = "/home/user/build_order.txt"

    assert os.path.isfile(deps_path), f"File {deps_path} does not exist."
    assert os.path.isfile(build_order_path), f"File {build_order_path} does not exist."

    with open(deps_path, 'r') as f:
        deps = json.load(f)

    with open(build_order_path, 'r') as f:
        order_str = f.read().strip()

    assert order_str, "build_order.txt is empty."

    order = [x.strip() for x in order_str.split(',')]

    expected_modules = set(deps.keys())
    actual_modules = set(order)

    assert expected_modules == actual_modules, f"Build order modules do not match expected. Expected: {expected_modules}, Got: {actual_modules}"
    assert len(order) == len(expected_modules), "Build order contains duplicate modules."

    seen = set()
    for module in order:
        module_deps = deps.get(module, [])
        for d in module_deps:
            assert d in seen, f"Dependency '{d}' of module '{module}' appears after it in the build order."
        seen.add(module)

def test_critical_path_correct():
    cp_path = "/home/user/critical_path.txt"
    assert os.path.isfile(cp_path), f"File {cp_path} does not exist."

    with open(cp_path, 'r') as f:
        cp_str = f.read().strip()

    assert cp_str == "48", f"Critical path value is incorrect. Expected '48', got '{cp_str}'."