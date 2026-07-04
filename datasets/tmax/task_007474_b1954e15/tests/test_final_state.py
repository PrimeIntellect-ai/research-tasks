# test_final_state.py

import os
import subprocess

def test_qa_env_directory_exists():
    """Verify that the working directory was created."""
    assert os.path.isdir("/home/user/qa_env"), "/home/user/qa_env directory is missing."

def test_input_files_exist():
    """Verify that the input files exist."""
    assert os.path.isfile("/home/user/qa_env/inputs/file1.txt"), "file1.txt is missing."
    assert os.path.isfile("/home/user/qa_env/inputs/file2.txt"), "file2.txt is missing."

def test_shared_library_exists_and_exports_symbol():
    """Verify libqa.so exists and exports process_data."""
    lib_path = "/home/user/qa_env/libqa.so"
    assert os.path.isfile(lib_path), f"{lib_path} is missing."

    # Check if process_data is exported using nm or objdump
    try:
        output = subprocess.check_output(["nm", "-D", lib_path], stderr=subprocess.STDOUT, text=True)
        assert "process_data" in output, f"Symbol 'process_data' not found in {lib_path}."
    except FileNotFoundError:
        # Fallback to objdump if nm is not available
        output = subprocess.check_output(["objdump", "-T", lib_path], stderr=subprocess.STDOUT, text=True)
        assert "process_data" in output, f"Symbol 'process_data' not found in {lib_path}."

def test_golden_file_contents():
    """Verify the contents of golden.txt."""
    golden_path = "/home/user/qa_env/golden.txt"
    assert os.path.isfile(golden_path), f"{golden_path} is missing."

    expected_lines = [
        "6170706c65",
        "62616e616e61",
        "6d616e676f",
        "7a65627261"
    ]

    with open(golden_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "golden.txt does not contain the correct hex-encoded output."

def test_output_file_matches_golden():
    """Verify that output.txt matches golden.txt exactly."""
    output_path = "/home/user/qa_env/output.txt"
    golden_path = "/home/user/qa_env/golden.txt"

    assert os.path.isfile(output_path), f"{output_path} is missing."

    with open(golden_path, "r") as f:
        golden_content = f.read()

    with open(output_path, "r") as f:
        output_content = f.read()

    assert output_content == golden_content, "output.txt does not exactly match golden.txt."

def test_test_result_log_is_empty():
    """Verify that test_result.log exists and is exactly 0 bytes."""
    log_path = "/home/user/qa_env/test_result.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."

    size = os.path.getsize(log_path)
    assert size == 0, f"{log_path} is not empty (size is {size} bytes)."

def test_test_runner_script():
    """Verify test_runner.py exists and imports ctypes."""
    script_path = "/home/user/qa_env/test_runner.py"
    assert os.path.isfile(script_path), f"{script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "ctypes" in content, "test_runner.py does not contain 'ctypes'."