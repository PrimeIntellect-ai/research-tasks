# test_final_state.py
import os
import subprocess
import pytest

def test_tinyserver_patched_exists_and_executable():
    binary_path = "/home/user/tinyserver_patched"
    assert os.path.isfile(binary_path), f"The patched binary does not exist at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"The patched binary at {binary_path} is not executable."

def test_evaluation_score():
    binary_path = "/home/user/tinyserver_patched"
    eval_script = "/app/evaluate_server.py"

    assert os.path.isfile(eval_script), f"Evaluation script {eval_script} is missing."

    try:
        out = subprocess.check_output(
            ["python3", eval_script, binary_path],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=30
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Evaluation script failed with exit code {e.returncode}. Output:\n{e.output}")
    except subprocess.TimeoutExpired:
        pytest.fail("Evaluation script timed out. The server might be hanging or crashing.")

    score = None
    for line in out.splitlines():
        if "SCORE:" in line:
            try:
                score = float(line.split("SCORE:")[1].strip())
                break
            except ValueError:
                continue

    assert score is not None, f"Could not find 'SCORE:' in the evaluation output. Output:\n{out}"
    assert score >= 1.0, f"Expected accuracy score >= 1.0, but got {score}. Output:\n{out}"