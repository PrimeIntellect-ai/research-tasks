# test_final_state.py
import os
import subprocess

def test_result_txt():
    """Test that result.txt exists and contains the correct hash output."""
    result_path = "/home/user/polybuild/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "64923478", f"Expected '64923478' in result.txt, but got '{content}'."

def test_valgrind_log():
    """Test that valgrind.log exists and shows no definite memory leaks."""
    log_path = "/home/user/polybuild/valgrind.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    # Valgrind output varies slightly but typically includes one of these when clean:
    no_leaks = (
        "definitely lost: 0 bytes in 0 blocks" in content or
        "All heap blocks were freed -- no leaks are possible" in content
    )
    assert no_leaks, "Valgrind log does not indicate that memory leaks were resolved (expected 0 bytes definitely lost)."

def test_shared_library():
    """Test that libpolyhash.so is correctly built as a shared object library."""
    lib_path = "/home/user/polybuild/libpolyhash.so"
    assert os.path.isfile(lib_path), f"File {lib_path} is missing."

    # Use the 'file' command to verify it's a shared object
    result = subprocess.run(["file", lib_path], capture_output=True, text=True)
    assert "shared object" in result.stdout, f"{lib_path} is not a valid shared object library. 'file' output: {result.stdout}"

def test_test_runner_executable():
    """Test that test_runner is built and executable."""
    runner_path = "/home/user/polybuild/test_runner"
    assert os.path.isfile(runner_path), f"File {runner_path} is missing."
    assert os.access(runner_path, os.X_OK), f"File {runner_path} is not executable."