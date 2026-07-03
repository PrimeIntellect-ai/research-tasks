# test_final_state.py

import os
import csv
import time
import subprocess
from collections import defaultdict

def test_makefile_fixed():
    makefile_path = "/app/sqlite-src-3410200/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-DSQLITE_OMIT_CTE=1" not in content, "Makefile still contains -DSQLITE_OMIT_CTE=1"
    assert "-DSQLITE_OMIT_WINDOWFUNC=1" not in content, "Makefile still contains -DSQLITE_OMIT_WINDOWFUNC=1"

def test_sqlite_compiled():
    binary_path = "/app/sqlite-src-3410200/sqlite3"
    assert os.path.isfile(binary_path), f"Compiled sqlite3 binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), "sqlite3 binary is not executable"

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), "Script is not executable"

def test_execution_time_and_output():
    script_path = "/home/user/analyze.sh"
    output_csv = "/home/user/top_performers.csv"

    # Remove output to ensure it's regenerated
    if os.path.exists(output_csv):
        os.remove(output_csv)

    start_time = time.time()
    result = subprocess.run([script_path], capture_output=True, text=True)
    duration = time.time() - start_time

    assert result.returncode == 0, f"analyze.sh failed with error:\n{result.stderr}"
    assert duration <= 15.0, f"Execution time {duration:.2f}s exceeded the 15.0s threshold"
    assert os.path.isfile(output_csv), f"Output CSV not generated at {output_csv}"

def test_data_correctness():
    output_csv = "/home/user/top_performers.csv"
    input_csv = "/home/user/sales_data.csv"

    # Parse input data
    data = {}
    children = defaultdict(list)
    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp = int(row['emp_id'])
            mgr = int(row['manager_id']) if row['manager_id'] else None
            dept = int(row['dept_id'])
            sales = float(row['individual_sales'])
            data[emp] = {'mgr': mgr, 'dept': dept, 'sales': sales, 'total': 0}
            if mgr is not None:
                children[mgr].append(emp)

    # Compute totals
    def get_total(emp):
        total = data[emp]['sales']
        for child in children[emp]:
            total += get_total(child)
        data[emp]['total'] = total
        return total

    # Find root(s)
    roots = [emp for emp, info in data.items() if info['mgr'] is None]
    for root in roots:
        get_total(root)

    dept_emps = defaultdict(list)
    for emp, info in data.items():
        dept_emps[info['dept']].append((info['total'], emp))

    expected = []
    for dept, emps in dept_emps.items():
        emps.sort(key=lambda x: (-x[0], x[1]))
        current_rank = 1
        for i in range(len(emps)):
            if i > 0 and emps[i][0] < emps[i-1][0]:
                current_rank = i + 1
            if current_rank <= 3:
                expected.append({
                    'emp_id': emps[i][1],
                    'dept_id': dept,
                    'total_team_sales': emps[i][0],
                    'dept_rank': current_rank
                })

    expected.sort(key=lambda x: (x['dept_id'], x['dept_rank'], x['emp_id']))

    # Read generated output
    actual = []
    with open(output_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            actual.append({
                'emp_id': int(row['emp_id']),
                'dept_id': int(row['dept_id']),
                'total_team_sales': float(row['total_team_sales']),
                'dept_rank': int(row['dept_rank'])
            })

    # We check if actual matches expected
    assert len(actual) == len(expected), f"Row count mismatch. Expected {len(expected)}, got {len(actual)}"

    for i, (act, exp) in enumerate(zip(actual, expected)):
        assert act['emp_id'] == exp['emp_id'], f"Row {i}: emp_id mismatch. Expected {exp['emp_id']}, got {act['emp_id']}"
        assert act['dept_id'] == exp['dept_id'], f"Row {i}: dept_id mismatch. Expected {exp['dept_id']}, got {act['dept_id']}"
        assert act['dept_rank'] == exp['dept_rank'], f"Row {i}: dept_rank mismatch. Expected {exp['dept_rank']}, got {act['dept_rank']}"
        assert abs(act['total_team_sales'] - exp['total_team_sales']) < 1e-5, f"Row {i}: total_team_sales mismatch. Expected {exp['total_team_sales']}, got {act['total_team_sales']}"