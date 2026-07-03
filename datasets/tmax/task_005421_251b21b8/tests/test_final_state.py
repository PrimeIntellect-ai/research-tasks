# test_final_state.py

import os
import subprocess
import pytest

def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def expected_sum(a, b):
    return sum(collatz_steps(i) for i in range(a, b + 1))

def test_script_exists_and_executable():
    script_path = "/home/user/ci_build_id.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable. Run 'chmod +x {script_path}'."

@pytest.mark.parametrize("a, b", [
    (10, 20),
    (1, 5),
    (50, 60),
])
def test_script_output(a, b):
    script_path = "/home/user/ci_build_id.sh"
    expected = expected_sum(a, b)

    try:
        result = subprocess.run([script_path, str(a), str(b)], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script timed out when processing range [{a}, {b}].")

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. stderr: {result.stderr}"

    output = result.stdout.strip()
    assert output == str(expected), f"Expected output '{expected}' for range [{a}, {b}], but got '{output}'."