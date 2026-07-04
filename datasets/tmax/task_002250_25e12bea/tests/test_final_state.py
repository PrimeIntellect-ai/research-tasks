# test_final_state.py
import os
import stat

def test_c_source_exists():
    """Test that the C source file exists."""
    assert os.path.exists("/home/user/analyze.c"), "The source file /home/user/analyze.c does not exist."
    assert os.path.isfile("/home/user/analyze.c"), "/home/user/analyze.c is not a regular file."

def test_executable_exists_and_executable():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/analyze"
    assert os.path.exists(exe_path), f"The executable {exe_path} does not exist."
    assert os.path.isfile(exe_path), f"{exe_path} is not a regular file."

    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file {exe_path} is not executable."

def test_anomalies_output():
    """Test that the anomalies.txt file contains the correct output."""
    output_path = "/home/user/anomalies.txt"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist. Did you run the program and redirect output?"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    expected_output = "Anomaly: 50\nAnomaly: 100"

    # Normalize line endings and whitespace
    actual_lines = [line.strip() for line in content.split('\n') if line.strip()]
    expected_lines = [line.strip() for line in expected_output.split('\n') if line.strip()]

    assert actual_lines == expected_lines, f"The contents of {output_path} do not match the expected anomalies. Found: {actual_lines}"