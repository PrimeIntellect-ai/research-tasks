# test_final_state.py
import os
import subprocess

def test_build_py_fixed():
    """Verify that build.py runs successfully and prints 'Build complete'."""
    build_script = "/home/user/app/build.py"
    assert os.path.isfile(build_script), f"{build_script} does not exist."

    result = subprocess.run(
        ["python3", build_script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"build.py failed with exit code {result.returncode}. stderr: {result.stderr}"
    assert "Build complete" in result.stdout, "build.py did not print 'Build complete'."

def test_crash_ref_extracted():
    """Verify that crash_ref.txt contains the correct extracted ID."""
    crash_ref_file = "/home/user/crash_ref.txt"
    assert os.path.isfile(crash_ref_file), f"{crash_ref_file} does not exist."

    with open(crash_ref_file, "r") as f:
        content = f.read().strip()

    assert content == "ERR-9482-SYS", f"Expected 'ERR-9482-SYS' in {crash_ref_file}, but got '{content}'."

def test_regression_test_passes():
    """Verify that test_regression.py exists and passes as a unittest."""
    test_script = "/home/user/app/test_regression.py"
    assert os.path.isfile(test_script), f"{test_script} does not exist."

    # Run the unittest module on the test file
    result = subprocess.run(
        ["python3", "-m", "unittest", "test_regression.py"],
        cwd="/home/user/app",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Regression test failed with exit code {result.returncode}. Output: {result.stderr or result.stdout}"

    # Also verify the test file imports process and uses the correct ID
    with open(test_script, "r") as f:
        content = f.read()

    assert "process" in content, "test_regression.py does not seem to import or use the 'process' function."
    assert "ERR-9482-SYS" in content, "test_regression.py does not contain the correct crash reference ID."
    assert "RuntimeError" in content, "test_regression.py does not assert a RuntimeError."