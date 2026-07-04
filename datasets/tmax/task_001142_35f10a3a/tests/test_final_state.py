# test_final_state.py
import os
import csv
import sqlite3
import stat
import pytest

def get_expected_data(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Find all HIGH sensitivity accesses per employee
    cursor.execute("""
        SELECT a.emp_id, e.name, e.department, a.resource_id
        FROM access_logs a
        JOIN resources r ON a.resource_id = r.resource_id
        JOIN employees e ON a.emp_id = e.emp_id
        WHERE r.sensitivity = 'HIGH'
    """)
    rows = cursor.fetchall()

    # Aggregate HIGH accesses per employee
    emp_stats = {}
    dept_high_accesses = {}
    emp_resources = {}

    for row in rows:
        emp_id = row['emp_id']
        dept = row['department']
        res_id = row['resource_id']

        if emp_id not in emp_stats:
            emp_stats[emp_id] = {
                'name': row['name'],
                'department': dept,
                'high_risk_accesses': 0
            }
            emp_resources[emp_id] = set()
            if dept not in dept_high_accesses:
                dept_high_accesses[dept] = []

        emp_stats[emp_id]['high_risk_accesses'] += 1
        emp_resources[emp_id].add(res_id)

    # Compute department averages for employees with >=1 HIGH access
    for dept in dept_high_accesses:
        accesses = [stats['high_risk_accesses'] for eid, stats in emp_stats.items() if stats['department'] == dept]
        dept_avg = sum(accesses) / len(accesses) if accesses else 0
        dept_high_accesses[dept] = round(dept_avg, 2)

    # Compute co-access degree
    expected_rows = []
    for emp_id, stats in emp_stats.items():
        my_resources = emp_resources[emp_id]
        co_access_degree = 0
        for other_emp_id, other_resources in emp_resources.items():
            if emp_id != other_emp_id:
                if my_resources.intersection(other_resources):
                    co_access_degree += 1

        expected_rows.append({
            'emp_id': emp_id,
            'name': stats['name'],
            'department': stats['department'],
            'high_risk_accesses': stats['high_risk_accesses'],
            'dept_avg_accesses': dept_high_accesses[stats['department']],
            'co_access_degree': co_access_degree
        })

    conn.close()

    # Sort by co_access_degree DESC, high_risk_accesses DESC, emp_id ASC
    expected_rows.sort(key=lambda x: (-x['co_access_degree'], -x['high_risk_accesses'], x['emp_id']))
    return expected_rows

def test_script_exists_and_executable():
    script_path = "/home/user/run_audit.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_csv_output():
    csv_path = "/home/user/audit_report.csv"
    db_path = "/home/user/audit.db"

    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist. Did the script run successfully?"
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    expected_data = get_expected_data(db_path)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, "CSV file is empty."

    header = reader[0]
    expected_header = ['emp_id', 'name', 'department', 'high_risk_accesses', 'dept_avg_accesses', 'co_access_degree']
    assert header == expected_header, f"CSV header mismatch. Expected {expected_header}, got {header}."

    assert len(reader) - 1 == len(expected_data), f"Expected {len(expected_data)} rows, got {len(reader) - 1}."

    for i, (actual_row, expected_row) in enumerate(zip(reader[1:], expected_data)):
        assert int(actual_row[0]) == expected_row['emp_id'], f"Row {i+1}: emp_id mismatch."
        assert actual_row[1] == expected_row['name'], f"Row {i+1}: name mismatch."
        assert actual_row[2] == expected_row['department'], f"Row {i+1}: department mismatch."
        assert int(actual_row[3]) == expected_row['high_risk_accesses'], f"Row {i+1}: high_risk_accesses mismatch."
        assert abs(float(actual_row[4]) - expected_row['dept_avg_accesses']) <= 0.01, f"Row {i+1}: dept_avg_accesses mismatch."
        assert int(actual_row[5]) == expected_row['co_access_degree'], f"Row {i+1}: co_access_degree mismatch."