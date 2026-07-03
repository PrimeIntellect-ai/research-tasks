# test_final_state.py
import os

def test_ensemble_script_exists_and_executable():
    script_path = '/home/user/ensemble_run.sh'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_all_runs_log():
    log_path = '/home/user/all_runs.log'
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 25, f"Expected exactly 25 lines in {log_path}, found {len(lines)}."

    for line in lines:
        assert line.startswith("Cost: "), f"Line in {log_path} does not start with 'Cost: '. Line: {line}"
        assert ", Path: " in line, f"Line in {log_path} does not contain ', Path: '. Line: {line}"

def test_best_model_output():
    log_path = '/home/user/all_runs.log'
    best_path_file = '/home/user/best_model.txt'

    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    assert os.path.exists(best_path_file), f"Best model file {best_path_file} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    min_cost = float('inf')
    best_path = ""
    best_cost_str = ""

    for line in lines:
        parts = line.split(', Path: ')
        assert len(parts) == 2, f"Malformed line in {log_path}: {line}"

        cost_str = parts[0].replace('Cost: ', '').strip()
        path_str = parts[1].strip()

        try:
            cost_val = float(cost_str)
        except ValueError:
            assert False, f"Could not parse cost as float: {cost_str}"

        if cost_val < min_cost:
            min_cost = cost_val
            best_path = path_str
            best_cost_str = cost_str

    with open(best_path_file, 'r') as f:
        best_lines = [line.strip() for line in f if line.strip()]

    assert len(best_lines) == 2, f"Expected exactly 2 lines in {best_path_file}, found {len(best_lines)}."
    assert best_lines[0] == f"Lowest Cost: {best_cost_str}", f"Expected 'Lowest Cost: {best_cost_str}', got '{best_lines[0]}'"
    assert best_lines[1] == f"Best Path: {best_path}", f"Expected 'Best Path: {best_path}', got '{best_lines[1]}'"