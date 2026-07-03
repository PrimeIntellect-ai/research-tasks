# test_final_state.py
import os
import stat

def test_run_sh_exists_and_executable():
    path = '/home/user/run.sh'
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_analyze_py_exists():
    path = '/home/user/analyze.py'
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_solution_txt():
    path = '/home/user/solution.txt'
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {path} is empty."

    parts = content.split(',')
    assert len(parts) == 2, f"Expected 2 comma-separated values in {path}, got {len(parts)}."

    try:
        x_val = float(parts[0])
        y_val = float(parts[1])
    except ValueError:
        assert False, f"Could not parse floats from {content}."

    expected_x = -0.435759
    expected_y = 0.360155
    tolerance = 1e-3

    assert abs(x_val - expected_x) < tolerance, f"Expected x to be near {expected_x}, got {x_val}"
    assert abs(y_val - expected_y) < tolerance, f"Expected y to be near {expected_y}, got {y_val}"