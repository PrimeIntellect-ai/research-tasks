# test_final_state.py
import os
import csv
import math

def test_generate_data_script_exists():
    assert os.path.exists("/home/user/generate_data.py"), "The script /home/user/generate_data.py does not exist."

def test_solution_plot_exists():
    assert os.path.exists("/home/user/solution.png"), "The plot /home/user/solution.png does not exist."

def test_converged_data_csv():
    csv_path = "/home/user/converged_data.csv"
    assert os.path.exists(csv_path), f"The CSV file {csv_path} does not exist."

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 42, f"Expected 42 lines in the CSV (1 header + 41 data rows), but got {len(rows)}."

    headers = [h.strip() for h in rows[0]]
    expected_headers = ["x", "u_num", "u_exact", "error"]
    assert headers == expected_headers, f"Expected headers {expected_headers}, but got {headers}."

    max_error = 0.0
    midpoint_found = False

    for row in rows[1:]:
        assert len(row) == 4, f"Row {row} does not have exactly 4 columns."
        try:
            x = float(row[0])
            u_num = float(row[1])
            u_exact = float(row[2])
            error = float(row[3])
        except ValueError:
            assert False, f"Could not parse row values as floats: {row}"

        # Check error calculation
        expected_error = abs(u_num - u_exact)
        assert math.isclose(error, expected_error, rel_tol=1e-5, abs_tol=1e-8), f"Error column {error} does not match abs(u_num - u_exact) {expected_error} at x={x}."

        if error > max_error:
            max_error = error

        # Check exact solution matches math.sin(pi * x)
        expected_u_exact = math.sin(math.pi * x)
        assert math.isclose(u_exact, expected_u_exact, rel_tol=1e-5, abs_tol=1e-8), f"u_exact {u_exact} does not match expected {expected_u_exact} at x={x}."

        # Check midpoint
        if math.isclose(x, 0.5, rel_tol=1e-5, abs_tol=1e-5):
            midpoint_found = True
            assert math.isclose(u_exact, 1.0, rel_tol=1e-5, abs_tol=1e-5), f"Expected u_exact at x=0.5 to be 1.0, got {u_exact}."
            assert math.isclose(u_num, 1.000514, rel_tol=1e-3, abs_tol=1e-3), f"Expected u_num at x=0.5 to be approx 1.000514, got {u_num}."

    assert midpoint_found, "Midpoint x=0.5 was not found in the CSV data."
    assert max_error < 1.0e-3, f"Maximum error {max_error} is not strictly less than 1.0e-3."
    assert max_error > 0.0, "Maximum error should be greater than 0 (numerical solution should not be perfectly exact)."