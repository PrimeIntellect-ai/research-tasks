# test_final_state.py

import os
import subprocess

def test_fix_link_script_exists():
    """Verify that the orchestration script exists."""
    script_path = "/home/user/fix_link.py"
    assert os.path.isfile(script_path), f"Expected script not found at {script_path}"

def test_bridge_assembly_exists():
    """Verify that the generated assembly file exists."""
    bridge_path = "/home/user/bridge.s"
    assert os.path.isfile(bridge_path), f"Expected assembly file not found at {bridge_path}"

def test_app_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    app_path = "/home/user/app"
    assert os.path.isfile(app_path), f"Expected executable not found at {app_path}"
    assert os.access(app_path, os.X_OK), f"File at {app_path} is not executable"

def test_output_log_content():
    """Verify that the test output log exists and contains the correct result."""
    log_path = "/home/user/test_output.log"
    assert os.path.isfile(log_path), f"Expected log file not found at {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    expected_output = "Result: 11\n"
    assert content == expected_output, f"Log file content is incorrect. Expected {repr(expected_output)}, got {repr(content)}"

def test_app_runs_correctly():
    """Verify that the compiled app runs correctly and produces the expected output."""
    app_path = "/home/user/app"
    try:
        result = subprocess.run([app_path], capture_output=True, text=True, check=True)
        assert result.stdout == "Result: 11\n", f"App output is incorrect. Expected 'Result: 11\\n', got {repr(result.stdout)}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing {app_path} failed with return code {e.returncode} and stderr: {e.stderr}")
    except OSError as e:
        pytest.fail(f"Failed to execute {app_path}: {e}")