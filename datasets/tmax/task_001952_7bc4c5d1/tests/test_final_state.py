# test_final_state.py

import os
import re
import stat
import pytest

def test_python_script_exists():
    """Test that the python script was created."""
    assert os.path.isfile('/home/user/clean_and_tune.py'), "The file /home/user/clean_and_tune.py does not exist."

def test_bash_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"The file {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file {script_path} is not executable."

def test_bash_script_environment_variables():
    """Test that the bash script exports the required environment variables."""
    script_path = '/home/user/run_pipeline.sh'
    with open(script_path, 'r') as f:
        content = f.read()

    required_vars = [
        r'OMP_NUM_THREADS\s*=\s*1',
        r'OPENBLAS_NUM_THREADS\s*=\s*1',
        r'MKL_NUM_THREADS\s*=\s*1',
        r'PYTHONHASHSEED\s*=\s*42'
    ]

    for var in required_vars:
        assert re.search(var, content), f"The bash script must set {var.split('=')[0].strip()}."

def test_reproducibility_log_format_and_content():
    """Test that the reproducibility log exists and has the correct format."""
    log_path = '/home/user/reproducibility_log.txt'
    assert os.path.isfile(log_path), f"The file {log_path} does not exist. Did you run the pipeline?"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}."

    assert lines[0].startswith("Best max_depth: "), "First line must start with 'Best max_depth: '"
    assert lines[1].startswith("Best CV score: "), "Second line must start with 'Best CV score: '"

    try:
        depth = int(lines[0].split(":")[1].strip())
    except ValueError:
        pytest.fail("Could not parse integer for Best max_depth.")

    try:
        score = float(lines[1].split(":")[1].strip())
    except ValueError:
        pytest.fail("Could not parse float for Best CV score.")

    # Check if the float has up to 4 decimal places
    score_str = lines[1].split(":")[1].strip()
    if '.' in score_str:
        assert len(score_str.split('.')[1]) <= 4, "The CV score must be rounded to 4 decimal places."