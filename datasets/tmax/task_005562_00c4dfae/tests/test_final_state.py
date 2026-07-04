# test_final_state.py

import os
import glob
import subprocess

def test_pytest_passes():
    """Verify that the pytest suite runs successfully."""
    result = subprocess.run(
        ["pytest", "/home/user/project/test_main.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_wheel_generated():
    """Verify that exactly one .whl file exists in the ci_artifacts directory."""
    wheels = glob.glob("/home/user/ci_artifacts/*.whl")
    assert len(wheels) == 1, f"Expected exactly 1 .whl file in /home/user/ci_artifacts, found {len(wheels)}: {wheels}"

def test_symbols_extracted():
    """Verify that symbols.txt exists and contains the PyInit_rate_limiter symbol."""
    symbols_file = "/home/user/ci_artifacts/symbols.txt"
    assert os.path.isfile(symbols_file), f"{symbols_file} does not exist. Ensure you ran nm -D and redirected the output."

    with open(symbols_file, "r") as f:
        content = f.read()

    assert "PyInit_rate_limiter" in content, "The symbol 'PyInit_rate_limiter' was not found in symbols.txt."