# test_final_state.py
import os
import subprocess

def test_solution_txt_content():
    path = "/home/user/solution.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "1020", f"Expected solution.txt to contain '1020', but found '{content}'"

def test_event_parser_compiled_and_fixed():
    executable = "/home/user/event_parser"
    assert os.path.isfile(executable), f"Executable {executable} does not exist. Did you recompile?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

    # Test the specific case requested
    try:
        result = subprocess.run([executable, "0", "4", "-8"], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        assert output == "1020", f"Expected output '1020' for inputs 0 4 -8, but got '{output}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Program crashed or returned non-zero exit code for inputs 0 4 -8. Error: {e.stderr}")

    # Test another negative case to ensure the fix is general
    try:
        result = subprocess.run([executable, "0", "0", "-1"], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        assert output == "1023", f"Expected output '1023' for inputs 0 0 -1, but got '{output}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Program crashed or returned non-zero exit code for inputs 0 0 -1. Error: {e.stderr}")

    # Test a normal positive case
    try:
        result = subprocess.run([executable, "1", "0", "0"], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        assert output == "24", f"Expected output '24' for inputs 1 0 0, but got '{output}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Program crashed or returned non-zero exit code for inputs 1 0 0. Error: {e.stderr}")