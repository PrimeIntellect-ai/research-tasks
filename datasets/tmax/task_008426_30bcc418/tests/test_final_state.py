# test_final_state.py

import os
import subprocess
import pytest

def test_resolve_script_exists():
    script_path = "/home/user/resolve.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_symlinks_correct():
    active_libs_dir = "/home/user/active_libs"
    expected_links = {
        "libA.so": "libA_v1.so",
        "libB.so": "libB_v1.so",
        "libC.so": "libC_v1.so",
        "libD.so": "libD_v1.so"
    }

    for link_name, target_name in expected_links.items():
        link_path = os.path.join(active_libs_dir, link_name)
        assert os.path.islink(link_path), f"{link_path} is missing or is not a symlink."

        target = os.readlink(link_path)
        assert target_name in target, f"Symlink {link_path} does not point to {target_name}."

def test_solution_log_content():
    log_path = "/home/user/solution.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "libA_v1.so",
        "libB_v1.so",
        "libC_v1.so",
        "libD_v1.so"
    ]

    assert lines == expected_lines, f"Content of {log_path} is incorrect. Expected {expected_lines}, got {lines}."

def test_e2e_test_execution():
    e2e_path = "/home/user/e2e_test.py"
    try:
        result = subprocess.run(
            ["python3", e2e_path],
            capture_output=True,
            text=True,
            check=True
        )
        assert "Success! Feature works." in result.stdout, "e2e_test.py did not print the success message."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"e2e_test.py failed to execute. Return code: {e.returncode}. Output: {e.output}")