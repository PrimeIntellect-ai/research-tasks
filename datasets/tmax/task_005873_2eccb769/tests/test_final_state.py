# test_final_state.py

import os
import json
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/math-addon"
SRC_DIR = os.path.join(WORKSPACE_DIR, "src")
PACKAGE_JSON = os.path.join(WORKSPACE_DIR, "package.json")
MATH_CPP = os.path.join(SRC_DIR, "math.cpp")
LIBMATH_SO = os.path.join(SRC_DIR, "libmath.so")
SUCCESS_TXT = "/home/user/success.txt"

def test_success_file():
    assert os.path.isfile(SUCCESS_TXT), f"File {SUCCESS_TXT} does not exist. Did you run the test command and redirect the output?"
    with open(SUCCESS_TXT, "r") as f:
        content = f.read()
    assert "All property tests passed!" in content, f"{SUCCESS_TXT} does not contain the expected success message. Tests might have failed."

def test_shared_library():
    assert os.path.isfile(LIBMATH_SO), f"Shared library {LIBMATH_SO} does not exist. Did you compile it?"

    # Check if it is a valid shared object
    result = subprocess.run(["file", LIBMATH_SO], capture_output=True, text=True)
    assert "shared object" in result.stdout or "dynamically linked" in result.stdout, f"{LIBMATH_SO} does not appear to be a valid shared object."

def test_package_json_fixed():
    assert os.path.isfile(PACKAGE_JSON), f"File {PACKAGE_JSON} does not exist."
    with open(PACKAGE_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{PACKAGE_JSON} is not valid JSON.")

    deps = data.get("devDependencies", {})
    fast_check = deps.get("fast-check", "")
    assert "github:not-a-real-repo/fast-check-broken" not in fast_check, "package.json still contains the broken fast-check dependency."

    # Verify node_modules exists
    node_modules = os.path.join(WORKSPACE_DIR, "node_modules")
    assert os.path.isdir(node_modules), f"node_modules directory not found in {WORKSPACE_DIR}. Did you run npm install?"

def test_math_cpp_fixed():
    assert os.path.isfile(MATH_CPP), f"File {MATH_CPP} does not exist."
    with open(MATH_CPP, "r") as f:
        content = f.read()

    # The original bug was `b = b % a;`
    assert "b = b % a;" not in content.replace(" ", ""), "The logical flaw 'b = b % a;' is still present in math.cpp."