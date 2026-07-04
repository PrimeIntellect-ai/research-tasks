# test_final_state.py
import os
import subprocess
import math

def test_executable_exists():
    executable_path = "/home/user/trajectory/traj_calc"
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing. Did the build script succeed?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_build_script_fixed():
    build_script_path = "/home/user/trajectory/build.sh"
    assert os.path.isfile(build_script_path), f"File {build_script_path} is missing."
    with open(build_script_path, 'r') as f:
        content = f.read()
    assert "-lm" in content, "The build script does not link the math library (-lm)."

def test_fuzzer_passes():
    fuzzer_path = "/home/user/trajectory/fuzzer.sh"
    assert os.path.isfile(fuzzer_path), f"File {fuzzer_path} is missing."

    try:
        result = subprocess.run([fuzzer_path], cwd="/home/user/trajectory", capture_output=True, text=True, check=True)
        assert "FUZZER PASSED" in result.stdout, "Fuzzer script did not print 'FUZZER PASSED'."
    except subprocess.CalledProcessError as e:
        pytest_fail_msg = f"Fuzzer script failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}"
        assert False, pytest_fail_msg

def test_final_output_file():
    output_file_path = "/home/user/final_output.txt"
    assert os.path.isfile(output_file_path), f"Final output file {output_file_path} is missing."

    with open(output_file_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Content of {output_file_path} is not a valid floating point number: {content}"

    expected_val = 1e-07
    assert math.isclose(val, expected_val, rel_tol=1e-5), f"Expected value close to {expected_val}, but got {val} in {output_file_path}."