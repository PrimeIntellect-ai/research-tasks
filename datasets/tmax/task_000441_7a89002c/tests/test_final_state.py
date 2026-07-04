# test_final_state.py

import os

def test_executable_exists():
    executable_path = "/app/project/optimize_sensor"
    assert os.path.isfile(executable_path), f"The executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_liblbfgs_installed():
    lib_path_a = "/app/local/lib/liblbfgs.a"
    lib_path_so = "/app/local/lib/liblbfgs.so"
    assert os.path.isfile(lib_path_a) or os.path.isfile(lib_path_so), "liblbfgs was not installed to /app/local/lib."

def test_result_file_exists():
    result_path = "/app/project/result.txt"
    assert os.path.isfile(result_path), f"The result file {result_path} is missing."

def test_cost_threshold():
    result_path = "/app/project/result.txt"

    try:
        with open(result_path, 'r') as f:
            content = f.read()
    except Exception as e:
        assert False, f"Failed to read {result_path}: {e}"

    try:
        cost_str = content.split('Final cost:')[1].strip()
        cost = float(cost_str)
    except Exception as e:
        assert False, f"Failed to parse the final cost from {result_path}. Error: {e}\nFile content:\n{content}"

    assert cost <= 0.01, f"Metric threshold failed: Final cost {cost} is greater than the threshold of 0.01."