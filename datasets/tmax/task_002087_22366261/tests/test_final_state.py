# test_final_state.py

import os
import stat

def test_venv_exists():
    assert os.path.isdir('/home/user/venv'), "/home/user/venv directory does not exist. Did you create the virtual environment?"
    assert os.path.isfile('/home/user/venv/bin/activate') or os.path.isfile('/home/user/venv/bin/python'), "Virtual environment does not appear to be properly initialized."

def test_run_etl_sh_exists_and_correct():
    path = '/home/user/run_etl.sh'
    assert os.path.isfile(path), f"Missing file: {path}"

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable. Did you run chmod +x?"

    with open(path, 'r') as f:
        content = f.read()

    assert 'activate' in content or '/venv/bin/' in content, "run_etl.sh does not seem to use the virtual environment."
    assert 'OMP_NUM_THREADS=1' in content, "run_etl.sh does not set OMP_NUM_THREADS=1"
    assert 'OPENBLAS_NUM_THREADS=1' in content, "run_etl.sh does not set OPENBLAS_NUM_THREADS=1"
    assert 'python' in content and 'etl.py' in content, "run_etl.sh does not execute the etl.py script."

def test_etl_output_correct():
    path = '/home/user/etl_output.txt'
    assert os.path.isfile(path), f"Missing output file: {path}. Did you run the pipeline?"

    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"The content of {path} ('{content}') is not a valid float."

    # The expected output is approximately 0.8521 or -0.8521 depending on scikit-learn version/PCA sign
    expected_abs_val = 0.8521
    actual_abs_val = abs(val)

    assert abs(actual_abs_val - expected_abs_val) < 0.001, f"The output value {val} is incorrect. The data leakage might not be properly fixed, or the wrong split/random state was used."

def test_etl_py_fixed():
    path = '/home/user/etl.py'
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        content = f.read()

    assert "pca.fit_transform(X)" not in content, "The data leakage bug (fitting PCA on the entire dataset 'X') is still present in etl.py."
    assert "train_test_split(X," in content or "train_test_split(X " in content or "train_test_split" in content, "train_test_split seems to be missing."