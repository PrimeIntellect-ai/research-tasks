# test_final_state.py
import os
import json
import pytest

def test_output_results_exists_and_correct():
    output_path = "/home/user/output_results.json"
    inputs_path = "/home/user/repo/data/inputs.json"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.exists(inputs_path), f"Input file {inputs_path} does not exist."

    with open(inputs_path, "r") as f:
        try:
            inputs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {inputs_path} as JSON.")

    expected_results = []
    for item in inputs:
        x = item.get("input_x")
        y = item.get("input_y")
        assert x is not None and y is not None, "Input items must contain 'input_x' and 'input_y'."
        expected_results.append({
            "x": x,
            "y": y,
            "result": 3 * (x ** 2) + 2 * y
        })

    with open(output_path, "r") as f:
        try:
            outputs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {output_path} as JSON.")

    assert isinstance(outputs, list), f"Expected {output_path} to contain a JSON array."
    assert len(outputs) == len(expected_results), f"Expected {len(expected_results)} results, found {len(outputs)}."

    for i, (actual, expected) in enumerate(zip(outputs, expected_results)):
        assert actual == expected, f"Result at index {i} is incorrect. Expected {expected}, got {actual}."

def test_libraries_built():
    build_dir = "/home/user/repo/build"
    assert os.path.exists(build_dir), f"Build directory {build_dir} does not exist."

    mathwrap_so = os.path.join(build_dir, "libmathwrap.so")
    fastmath_so = os.path.join(build_dir, "libfastmath.so")

    assert os.path.exists(mathwrap_so), f"Library {mathwrap_so} was not built."
    assert os.path.exists(fastmath_so), f"Library {fastmath_so} was not built."

def test_cmakelists_fixed():
    cmakelists_path = "/home/user/repo/CMakeLists.txt"
    assert os.path.exists(cmakelists_path), f"File {cmakelists_path} does not exist."

    with open(cmakelists_path, "r") as f:
        content = f.read()

    assert "target_link_libraries" in content and "mathwrap" in content and "fastmath" in content, \
        "CMakeLists.txt does not appear to link mathwrap against fastmath."

def test_assembly_bug_fixed():
    asm_path = "/home/user/repo/src/fast_math.s"
    assert os.path.exists(asm_path), f"File {asm_path} does not exist."

    with open(asm_path, "r") as f:
        content = f.read()

    assert "add $2, %rcx" not in content, "The assembly bug (add $2, %rcx) is still present."