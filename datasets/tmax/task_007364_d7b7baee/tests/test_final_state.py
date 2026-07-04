# test_final_state.py
import os
import stat

def test_run_analysis_exists_and_executable():
    path = '/home/user/run_analysis.sh'
    assert os.path.isfile(path), f"{path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_peaks_file():
    path = '/home/user/peaks.txt'
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')
    assert len(lines) == 50, f"Expected 50 lines in {path}, found {len(lines)}."
    for line in lines:
        assert line.lstrip('-').isdigit(), f"Expected integer values in {path}, found '{line}'."

def test_positions_file():
    path = '/home/user/positions.txt'
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')
    assert len(lines) == 50, f"Expected 50 lines in {path}, found {len(lines)}."
    for line in lines:
        assert line.lstrip('-').isdigit(), f"Expected integer values in {path}, found '{line}'."

def test_notebook_exists():
    path = '/home/user/fit_model.ipynb'
    assert os.path.isfile(path), f"{path} is missing."

def test_slope_file():
    path = '/home/user/slope.txt'
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        slope = float(content)
    except ValueError:
        assert False, f"Could not parse '{content}' as a float in {path}."

    # The true slope is exactly 2.000
    assert abs(slope - 2.0) < 0.05, f"Expected slope to be around 2.000, found {slope}."