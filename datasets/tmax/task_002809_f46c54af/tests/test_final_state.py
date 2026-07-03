# test_final_state.py
import os
import subprocess

def test_test_results_log_exists():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did you save the test output?"

def test_test_results_log_content():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "PASS" in content, "The test_results.log does not contain 'PASS'."
    assert "FAIL" not in content, "The test_results.log contains 'FAIL'."

def test_go_test_passes():
    project_dir = "/home/user/aggregator"
    assert os.path.isdir(project_dir), f"Directory {project_dir} does not exist."

    result = subprocess.run(
        ["go", "test", "./..."],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"go test failed with return code {result.returncode}.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"