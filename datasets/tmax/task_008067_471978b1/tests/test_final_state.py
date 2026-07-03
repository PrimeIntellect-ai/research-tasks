# test_final_state.py
import os
import subprocess
import tempfile

def test_minimal_bug_csv():
    path = "/home/user/minimal_bug.csv"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ["100000000.1", "100000000.2"]
    assert lines == expected_lines, f"Content of {path} does not match the expected minimal bug lines. Expected {expected_lines}, got {lines}."

def test_bug_report_txt():
    path = "/home/user/bug_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "Failing line: 502"
    assert content == expected, f"Content of {path} is incorrect. Expected '{expected}', got '{content}'."

def test_regression_test_sh():
    path = "/home/user/regression_test.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    # Create a temporary file that triggers nan
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f_bad:
        f_bad.write("100000000.1\n100000000.2\n")
        bad_path = f_bad.name

    # Create a temporary file that does not trigger nan
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f_good:
        f_good.write("10.1\n10.2\n10.3\n")
        good_path = f_good.name

    try:
        # Test bad file
        result_bad = subprocess.run([path, bad_path], capture_output=True, text=True)
        assert result_bad.returncode == 1, f"Regression test should exit with status 1 for a file producing 'nan', got {result_bad.returncode}."

        output_bad = result_bad.stdout + result_bad.stderr
        assert "BUG DETECTED" in output_bad, f"Regression test should print 'BUG DETECTED' for a file producing 'nan'. Output was: {output_bad}"

        # Test good file
        result_good = subprocess.run([path, good_path], capture_output=True, text=True)
        assert result_good.returncode == 0, f"Regression test should exit with status 0 for a file with valid numbers, got {result_good.returncode}."

        output_good = result_good.stdout + result_good.stderr
        assert "PASS" in output_good, f"Regression test should print 'PASS' for a file with valid numbers. Output was: {output_good}"
    finally:
        os.remove(bad_path)
        os.remove(good_path)