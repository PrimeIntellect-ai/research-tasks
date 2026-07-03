# test_final_state.py
import os
import stat
import subprocess
import csv

def test_solver_executable_exists():
    solver_path = "/home/user/solver"
    assert os.path.isfile(solver_path), f"Executable {solver_path} does not exist."
    assert os.access(solver_path, os.X_OK), f"Executable {solver_path} is not executable."

def test_c_code_regularization():
    c_path = "/home/user/find_steady_state.c"
    assert os.path.isfile(c_path), f"C source file {c_path} is missing."
    with open(c_path, 'r') as f:
        content = f.read()

    # Check for regularization addition
    assert "1e-6" in content, "Regularization term '1e-6' not found in the C code."

def test_csv_format_and_values():
    csv_path = "/home/user/steady_state.csv"
    assert os.path.isfile(csv_path), f"CSV file {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 2, "CSV file must have at least a header row and a data row."
    assert rows[0] == ['x', 'y'], "CSV header must be exactly 'x,y'."

    try:
        x_val = float(rows[1][0])
        y_val = float(rows[1][1])
    except ValueError:
        assert False, "CSV data row must contain numeric values."

    # The analytical roots are x=0.5, y=0.5
    assert 0.49 < x_val < 0.51, f"Expected x value around 0.5, got {x_val}"
    assert 0.49 < y_val < 0.51, f"Expected y value around 0.5, got {y_val}"

def test_validate_script():
    script_path = "/home/user/validate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    output = result.stdout.strip()

    assert output == "VALID", f"Expected script to output 'VALID', got '{output}'"