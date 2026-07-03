# test_final_state.py

import os
import subprocess
import base64
import pytest

PROJECT_DIR = "/home/user/math_project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "run_pipeline.sh")

@pytest.fixture(scope="session", autouse=True)
def run_student_script():
    """Run the student's script before checking the state."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

    result = subprocess.run([SCRIPT_PATH], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute properly. Stderr: {result.stderr}"

def test_directories_created():
    for d in ["src", "bin", "results"]:
        path = os.path.join(PROJECT_DIR, d)
        assert os.path.isdir(path), f"Directory {path} was not created."

def test_source_files_moved():
    for f in ["main.c", "math_ops.c"]:
        old_path = os.path.join(PROJECT_DIR, f)
        new_path = os.path.join(PROJECT_DIR, "src", f)
        assert not os.path.exists(old_path), f"File {old_path} was not moved."
        assert os.path.isfile(new_path), f"File {new_path} does not exist in src directory."

def test_executable_compiled():
    bin_path = os.path.join(PROJECT_DIR, "bin", "calc")
    assert os.path.isfile(bin_path), f"Executable {bin_path} was not compiled."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_benchmark_file():
    bench_path = os.path.join(PROJECT_DIR, "results", "benchmark.txt")
    assert os.path.isfile(bench_path), f"Benchmark file {bench_path} does not exist."

    with open(bench_path, "r") as f:
        content = f.read()

    assert "real" in content, "Benchmark file missing 'real' timing."
    assert "user" in content, "Benchmark file missing 'user' timing."
    assert "sys" in content, "Benchmark file missing 'sys' timing."

def test_encoded_output():
    b64_path = os.path.join(PROJECT_DIR, "results", "encoded_out.b64")
    assert os.path.isfile(b64_path), f"Encoded output file {b64_path} does not exist."

    with open(b64_path, "r") as f:
        encoded_content = f.read().strip()

    try:
        decoded_bytes = base64.b64decode(encoded_content)
        decoded_text = decoded_bytes.decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to decode base64 content: {e}")

    # Run the compiled binary to get the expected output
    bin_path = os.path.join(PROJECT_DIR, "bin", "calc")
    result = subprocess.run([bin_path, "5000000"], capture_output=True, text=True)
    expected_output = result.stdout.strip()

    assert decoded_text == expected_output, f"Decoded output '{decoded_text}' does not match expected '{expected_output}'."