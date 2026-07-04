# test_final_state.py
import os
import json
import subprocess

def test_makefile_exists_and_flags():
    """Verify Makefile exists and contains required compiler flags."""
    makefile_path = "/home/user/Makefile"
    assert os.path.exists(makefile_path), f"Makefile not found at {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "g++" in content, "Makefile does not specify g++ as the compiler."
    assert "-std=c++17" in content, "Makefile does not contain the -std=c++17 flag."
    assert "-O2" in content, "Makefile does not contain the -O2 flag."

def test_build_executable():
    """Verify that running make produces the test_runner executable."""
    # Remove executable if it exists to ensure make actually builds it
    exe_path = "/home/user/test_runner"
    if os.path.exists(exe_path):
        os.remove(exe_path)

    result = subprocess.run(["make", "-C", "/home/user"], capture_output=True, text=True)
    assert result.returncode == 0, f"make command failed with output:\n{result.stderr}"
    assert os.path.exists(exe_path), f"Executable {exe_path} was not created by make."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_run_executable_and_output():
    """Verify that running test_runner produces the correct JSON output."""
    exe_path = "/home/user/test_runner"
    json_path = "/home/user/test_result.json"

    # Remove JSON if it exists to ensure test_runner actually creates it
    if os.path.exists(json_path):
        os.remove(json_path)

    result = subprocess.run([exe_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"test_runner failed with output:\n{result.stderr}"
    assert os.path.exists(json_path), f"Output file {json_path} was not created."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} does not contain valid JSON."

    assert "variance" in data, "JSON output missing 'variance' key."

    # The variance should be exactly 66.6667 as per the requirements
    variance = data["variance"]
    assert isinstance(variance, (int, float)), "Variance must be a numerical value."
    assert abs(variance - 66.6667) < 1e-5, f"Expected variance to be 66.6667, got {variance}"