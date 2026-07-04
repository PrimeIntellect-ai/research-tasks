# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/pipeline_diag"

def test_hanging_syscall_txt():
    file_path = os.path.join(BASE_DIR, "hanging_syscall.txt")
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip().lower()

    valid_syscalls = ["read", "wait4", "waitpid", "epoll_wait"]
    assert any(sc in content for sc in valid_syscalls), (
        f"hanging_syscall.txt does not contain a valid expected syscall (e.g., read, wait4). Found: {content}"
    )

def test_output_txt_matches_expected():
    output_path = os.path.join(BASE_DIR, "output.txt")
    expected_path = os.path.join(BASE_DIR, "expected.txt")

    assert os.path.isfile(output_path), f"File {output_path} is missing."
    assert os.path.isfile(expected_path), f"File {expected_path} is missing."

    with open(output_path, "r") as f:
        output_content = f.read().strip()

    with open(expected_path, "r") as f:
        expected_content = f.read().strip()

    assert output_content == expected_content, (
        f"output.txt does not match expected.txt.\n"
        f"Expected: {expected_content}\n"
        f"Actual: {output_content}"
    )

def test_final_diff_patch_empty():
    patch_path = os.path.join(BASE_DIR, "final_diff.patch")
    assert os.path.isfile(patch_path), f"File {patch_path} is missing."

    file_size = os.path.getsize(patch_path)
    assert file_size == 0, f"final_diff.patch is not empty (size: {file_size} bytes). It should be empty if output matches expected."

def test_run_pipeline_executes_successfully():
    script_path = os.path.join(BASE_DIR, "run_pipeline.py")
    input_path = os.path.join(BASE_DIR, "input.json")

    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    try:
        result = subprocess.run(
            ["python3", script_path, input_path],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("run_pipeline.py timed out. The infinite loop or deadlock is not fully fixed.")

    assert result.returncode == 0, f"run_pipeline.py failed with return code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    expected_sum = "SUM: 15.617283945"
    assert output == expected_sum, f"run_pipeline.py produced incorrect output. Expected '{expected_sum}', got '{output}'"