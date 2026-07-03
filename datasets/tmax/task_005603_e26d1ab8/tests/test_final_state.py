# test_final_state.py
import os
import stat
import subprocess
import re
import pytest

def test_evaluate_sh_exists_and_executable():
    """Check if evaluate.sh exists and is executable."""
    script_path = '/home/user/evaluate.sh'
    assert os.path.isfile(script_path), f"File not found: {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

def test_evaluate_sh_contents():
    """Check if evaluate.sh exports the required environment variables."""
    script_path = '/home/user/evaluate.sh'
    with open(script_path, 'r') as f:
        content = f.read()

    assert re.search(r'PYTHONHASHSEED\s*=\s*42', content), "evaluate.sh does not export PYTHONHASHSEED=42"
    assert re.search(r'OMP_NUM_THREADS\s*=\s*1', content), "evaluate.sh does not export OMP_NUM_THREADS=1"
    assert "pipeline.py" in content, "evaluate.sh does not execute pipeline.py"
    assert "accuracy.txt" in content, "evaluate.sh does not redirect output to accuracy.txt"

def test_pipeline_py_fixed():
    """Check if pipeline.py has the data leak fixed."""
    pipeline_path = '/home/user/pipeline.py'
    with open(pipeline_path, 'r') as f:
        content = f.read()

    # It should no longer fit_transform on the whole dataframe
    assert not re.search(r'fit_transform\(\s*df\[', content), "pipeline.py still fits on the entire dataset."

    # It should split first
    assert "train_test_split" in content, "train_test_split is missing."

    # It should fit_transform on the train set
    assert re.search(r'fit_transform\(.*train', content, re.IGNORECASE) or re.search(r'fit_transform\(.*X_train', content), "pipeline.py does not fit_transform on the training set."

def test_evaluate_sh_execution():
    """Run evaluate.sh and check if accuracy.txt is produced with a valid float."""
    script_path = '/home/user/evaluate.sh'
    out_path = '/home/user/accuracy.txt'

    # Remove accuracy.txt if it exists to ensure the script creates it
    if os.path.exists(out_path):
        os.remove(out_path)

    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"evaluate.sh failed to run. Stderr: {result.stderr}"

    assert os.path.isfile(out_path), f"{out_path} was not created by evaluate.sh"

    with open(out_path, 'r') as f:
        output = f.read().strip()

    try:
        accuracy = float(output)
    except ValueError:
        pytest.fail(f"accuracy.txt does not contain a valid float. Found: {output}")

    assert 0.0 <= accuracy <= 1.0, f"Accuracy {accuracy} is out of bounds [0.0, 1.0]"