# test_final_state.py

import os
import subprocess
import math
import pytest

def get_expected_result():
    # Recompute the expected value based on the git history
    # The key "1a2b3c" was hardcoded in commit 2
    seed = int("1a2b3c", 16)
    result = math.sqrt(seed) * 3.14159
    return f"{result:.2f}"

def test_result_file_exists_and_correct():
    result_file = "/home/user/result.txt"
    assert os.path.isfile(result_file), f"The result file {result_file} does not exist."

    with open(result_file, "r") as f:
        content = f.read().strip()

    expected = get_expected_result()
    assert content == expected, f"Expected the result file to contain '{expected}', but found '{content}'."

def test_executable_exists_and_runnable():
    executable = "/home/user/math_build/matrix_magic"
    assert os.path.isfile(executable), f"The compiled executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"The file {executable} is not executable."

    # Test running the executable with the correct environment variable
    env = os.environ.copy()
    env["MATH_API_KEY"] = "1a2b3c"

    try:
        result = subprocess.run(
            [executable],
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        expected = get_expected_result()
        assert output == expected, f"Running {executable} with correct MATH_API_KEY produced '{output}', expected '{expected}'."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running {executable} failed with return code {e.returncode} and stderr: {e.stderr}")

def test_build_script_fixes():
    build_script = "/home/user/math_build/build.sh"
    assert os.path.isfile(build_script), f"Build script {build_script} is missing."

    with open(build_script, "r") as f:
        content = f.read()

    # The build script should no longer use the deprecated v2 headers
    assert "-I./deps/v2" not in content, "The build script still includes the deprecated v2 headers (-I./deps/v2)."

    # The build script must link the math library
    assert "-lm" in content.split(), "The build script does not link the math library (-lm)."