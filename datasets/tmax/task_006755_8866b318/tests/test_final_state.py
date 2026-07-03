# test_final_state.py
import os
import csv

def process_matrices(csv_path):
    total = 0
    unstable = 0
    stable_accurate = 0
    stable_inaccurate = 0

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: 
                continue
            total += 1
            a = float(row[1])
            b = float(row[2])
            c = float(row[3])
            d = float(row[4])

            det = a * d - b * c
            if abs(det) < 1e-6:
                unstable += 1
            else:
                # Compute inverse
                inv_a = d / det
                inv_b = -b / det
                inv_c = -c / det
                inv_d = a / det

                # Compute product P = A * A^-1
                p11 = a * inv_a + b * inv_c
                p12 = a * inv_b + b * inv_d
                p21 = c * inv_a + d * inv_c
                p22 = c * inv_b + d * inv_d

                # Calculate max absolute error
                max_err = max(abs(p11 - 1.0), abs(p12 - 0.0), abs(p21 - 0.0), abs(p22 - 1.0))

                if max_err > 1e-9:
                    stable_inaccurate += 1
                else:
                    stable_accurate += 1

    return total, unstable, stable_accurate, stable_inaccurate

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_matrices.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable. Run 'chmod +x {script_path}'."

def test_report_content():
    csv_path = "/home/user/input/matrices.csv"
    assert os.path.isfile(csv_path), f"The input file {csv_path} is missing."

    total, unstable, stable_accurate, stable_inaccurate = process_matrices(csv_path)

    expected_lines = [
        f"Total Matrices: {total}",
        f"Unstable: {unstable}",
        f"Stable Accurate: {stable_accurate}",
        f"Stable Inaccurate: {stable_inaccurate}"
    ]

    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"The report file {report_path} does not exist."

    with open(report_path, "r") as f:
        report_content = f.read().strip().splitlines()

    assert len(report_content) == 4, f"The report should have exactly 4 lines, but found {len(report_content)} lines."

    for i, expected in enumerate(expected_lines):
        actual = report_content[i].strip()
        assert actual == expected, f"Line {i+1} of report is incorrect.\nExpected: '{expected}'\nActual: '{actual}'"