# test_final_state.py
import os
import stat
import subprocess
import tempfile

def test_script_exists_and_executable():
    script_path = "/home/user/fit_model.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_script_uses_awk():
    script_path = "/home/user/fit_model.sh"
    with open(script_path, "r") as f:
        content = f.read()
    assert "awk" in content, f"Script {script_path} does not appear to use 'awk' as required."

def test_result_file_content():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected = "m=2.000000,b=0.120000"
    assert content == expected, f"Content of {result_path} is incorrect. Expected '{expected}', got '{content}'."

def test_script_dynamic_computation():
    script_path = "/home/user/fit_model.sh"

    # Create a temporary CSV file with different data
    # x: 1, 2, 3
    # y: 2, 4, 6
    # expected: m=2.000000, b=0.000000
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
        tmp.write("x,y\n1,2\n2,4\n3,6\n")
        tmp_path = tmp.name

    try:
        result = subprocess.run([script_path, tmp_path], capture_output=True, text=True)
        assert result.returncode == 0, "Script failed to execute on test data."
        output = result.stdout.strip()
        expected_output = "m=2.000000,b=0.000000"
        assert output == expected_output, f"Script did not compute the correct OLS parameters for test data. Expected '{expected_output}', got '{output}'."
    finally:
        os.remove(tmp_path)