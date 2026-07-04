# test_final_state.py
import os
import subprocess
import pytest

def test_ci_output_file():
    output_file = "/home/user/ci_output.txt"
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist."
    with open(output_file, "r") as f:
        content = f.read()
    assert "CI SUCCESS: All tests passed." in content, f"Output file does not contain the success message. Content: {content}"

def test_router_cpp_fixes():
    filepath = "/home/user/MathRouter/src/router.cpp"
    assert os.path.isfile(filepath), f"{filepath} is missing"
    with open(filepath, "r") as f:
        content = f.read()

    assert "std::stoi" not in content, "The std::stoi bug is still present in router.cpp. It should be std::stod."
    assert "std::stod" in content or "stod" in content, "Expected to find stod in router.cpp for parsing doubles."

def test_test_router_cpp_fixes():
    filepath = "/home/user/MathRouter/tests/test_router.cpp"
    assert os.path.isfile(filepath), f"{filepath} is missing"
    with open(filepath, "r") as f:
        content = f.read()

    assert '{"result": 4.000000}' in content, "The expected output format in test_router.cpp is incorrect. It should expect 'result' instead of 'answer'."
    assert "fixture.initialized = true" in content or "initialized = true" in content or "setup()" in content, "The fixture is not properly initialized in test_router.cpp."

def test_ci_script_passes():
    ci_script = "/home/user/MathRouter/ci.sh"
    assert os.path.isfile(ci_script), f"{ci_script} is missing"

    result = subprocess.run([ci_script], cwd="/home/user/MathRouter", capture_output=True, text=True)
    assert result.returncode == 0, f"ci.sh failed with return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert "CI SUCCESS: All tests passed." in result.stdout, "ci.sh did not output the success message."