# test_final_state.py

import os
import stat
import pytest

def test_ci_result_log():
    """Check that ci_result.log contains CI_PASS."""
    log_path = "/home/user/polybuild/ci_result.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did the CI script run?"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "CI_PASS", f"Expected ci_result.log to contain 'CI_PASS', but found '{content}'."

def test_actual_version():
    """Check that actual_version.txt contains exactly 1.2.3."""
    version_path = "/home/user/polybuild/actual_version.txt"
    assert os.path.isfile(version_path), f"File {version_path} does not exist."
    with open(version_path, "r") as f:
        content = f.read().strip()
    assert content == "1.2.3", f"Expected actual_version.txt to contain '1.2.3', but found '{content}'."

def test_actual_data_and_expected():
    """Check actual_data.txt and expected.txt for the correct sorted output."""
    actual_path = "/home/user/polybuild/actual_data.txt"
    expected_path = "/home/user/polybuild/expected.txt"

    assert os.path.isfile(actual_path), f"File {actual_path} does not exist."
    assert os.path.isfile(expected_path), f"File {expected_path} does not exist."

    expected_lines = ["alpha", "bravo", "charlie", "zebra"]

    with open(actual_path, "r") as f:
        actual_content = [line.strip() for line in f.readlines() if line.strip()]

    with open(expected_path, "r") as f:
        expected_content = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_content == expected_lines, f"actual_data.txt does not contain the correctly sorted data. Found: {actual_content}"
    assert expected_content == expected_lines, f"expected.txt does not contain the correctly sorted data. Found: {expected_content}"

def test_ci_script_content_and_permissions():
    """Check that ci.sh exists, is executable, and contains the correct go build command."""
    script_path = "/home/user/polybuild/ci.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "go build" in content, "ci.sh does not contain a 'go build' command."
    assert "-ldflags" in content, "ci.sh does not use '-ldflags' in the build command."
    assert "main.Version=1.2.3" in content.replace("'", "").replace('"', ''), "ci.sh does not inject 'main.Version=1.2.3' correctly."

def test_go_project_files():
    """Check that the Go project files were created."""
    main_path = "/home/user/polybuild/main.go"
    mod_path = "/home/user/polybuild/go.mod"

    assert os.path.isfile(main_path), f"Go source file {main_path} does not exist."
    assert os.path.isfile(mod_path), f"Go module file {mod_path} does not exist."