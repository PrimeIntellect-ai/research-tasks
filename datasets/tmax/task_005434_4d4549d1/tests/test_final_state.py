# test_final_state.py

import os
import stat

def test_analyze_script_exists():
    """Test that the analyze.py script exists."""
    assert os.path.isfile('/home/user/analyze.py'), "Missing script: /home/user/analyze.py"

def test_top_pair_file():
    """Test that top_pair.txt exists and contains the correct result."""
    file_path = '/home/user/top_pair.txt'
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "D998,D999,0.8542", f"Incorrect content in {file_path}. Expected 'D998,D999,0.8542', got '{content}'"

def test_time_log():
    """Test that time.log exists and contains a valid float."""
    file_path = '/home/user/time.log'
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    try:
        time_val = float(content)
        assert time_val >= 0, f"Time value in {file_path} must be non-negative, got {time_val}"
    except ValueError:
        assert False, f"Content of {file_path} is not a valid float: '{content}'"

def test_reproducibility_script():
    """Test that test_reproducibility.sh exists and is executable."""
    file_path = '/home/user/test_reproducibility.sh'
    assert os.path.isfile(file_path), f"Missing script: {file_path}"

    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {file_path} is not executable"

def test_repro_result():
    """Test that repro_result.txt exists and contains PASS."""
    file_path = '/home/user/repro_result.txt'
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "PASS", f"Incorrect content in {file_path}. Expected 'PASS', got '{content}'"