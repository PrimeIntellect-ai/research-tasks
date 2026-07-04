# test_final_state.py

import os
import sqlite3
import csv
import json
import pytest

DB_PATH = "/home/user/company.db"
SQL_QUERY_PATH = "/home/user/fixed_query.sql"
RELATIONAL_CSV_PATH = "/home/user/relational_export.csv"
DOCUMENT_JSON_PATH = "/home/user/document_export.json"
GRAPH_NODES_PATH = "/home/user/graph_nodes.csv"
GRAPH_EDGES_PATH = "/home/user/graph_edges.csv"

@pytest.fixture(scope="module")
def db_data():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    data = {}

    cursor.execute("SELECT * FROM departments")
    data['departments'] = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM employees")
    data['employees'] = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM projects")
    data['projects'] = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM employee_projects")
    data['employee_projects'] = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return data

def test_fixed_query_exists():
    assert os.path.exists(SQL_QUERY_PATH), f"The file {SQL_QUERY_PATH} does not exist."

def test_relational_export(db_data):
    assert os.path.exists(RELATIONAL_CSV_PATH), f"The file {RELATIONAL_CSV_PATH} does not exist."

    # Compute expected
    expected_rows = []
    dept_map = {d['id']: d['name'] for d in db_data['departments']}
    emp_map = {e['id']: e for e in db_data['employees']}
    proj_map = {p['id']: p['name'] for p in db_data['projects']}

    for ep in db_data['employee_projects']:
        emp = emp_map[ep['emp_id']]
        dept_name = dept_map[emp['dept_id']]
        emp_name = emp['name']
        proj_name = proj_map[ep['proj_id']]
        expected_rows.append((emp_name, dept_name, proj_name))

    expected_rows.sort(key=lambda x: (x[0], x[2]))

    # Read actual
    with open(RELATIONAL_CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ['employee_name', 'department_name', 'project_name'], f"Incorrect headers in {RELATIONAL_CSV_PATH}"
        actual_rows = [tuple(row) for row in reader]

    assert actual_rows == expected_rows, f"Data in {RELATIONAL_CSV_PATH} does not match expected output."

def test_document_export(db_data):
    assert os.path.exists(DOCUMENT_JSON_PATH), f"The file {DOCUMENT_JSON_PATH} does not exist."

    # Compute expected
    dept_map = {d['id']: d['name'] for d in db_data['departments']}
    emp_map = {e['id']: e for e in db_data['employees']}
    proj_map = {p['id']: p['name'] for p in db_data['projects']}

    # Build hierarchy
    depts = {}
    for d in db_data['departments']:
        depts[d['id']] = {
            "department_id": d['id'],
            "department_name": d['name'],
            "employees": {}
        }

    for e in db_data['employees']:
        depts[e['dept_id']]['employees'][e['id']] = {
            "employee_id": e['id'],
            "employee_name": e['name'],
            "projects": []
        }

    for ep in db_data['employee_projects']:
        emp = emp_map[ep['emp_id']]
        proj_name = proj_map[ep['proj_id']]
        depts[emp['dept_id']]['employees'][ep['emp_id']]['projects'].append({
            "project_id": ep['proj_id'],
            "project_name": proj_name
        })

    expected_json = []
    for d_id in sorted(depts.keys()):
        dept_obj = depts[d_id]
        emp_list = []
        for e_id in sorted(dept_obj['employees'].keys()):
            emp_obj = dept_obj['employees'][e_id]
            emp_obj['projects'].sort(key=lambda x: x['project_id'])
            emp_list.append(emp_obj)
        dept_obj['employees'] = emp_list
        expected_json.append(dept_obj)

    # Read actual
    with open(DOCUMENT_JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {DOCUMENT_JSON_PATH} does not contain valid JSON.")

    assert actual_json == expected_json, f"JSON structure in {DOCUMENT_JSON_PATH} does not match the expected output."

def test_graph_export(db_data):
    assert os.path.exists(GRAPH_NODES_PATH), f"The file {GRAPH_NODES_PATH} does not exist."
    assert os.path.exists(GRAPH_EDGES_PATH), f"The file {GRAPH_EDGES_PATH} does not exist."

    # Compute expected nodes
    expected_nodes = []
    for d in db_data['departments']:
        expected_nodes.append((f"dept_{d['id']}", "Department", d['name']))
    for e in db_data['employees']:
        expected_nodes.append((f"emp_{e['id']}", "Employee", e['name']))
    for p in db_data['projects']:
        expected_nodes.append((f"proj_{p['id']}", "Project", p['name']))

    expected_nodes.sort(key=lambda x: (x[0], x[1]))

    # Compute expected edges
    expected_edges = []
    for e in db_data['employees']:
        expected_edges.append((f"emp_{e['id']}", f"dept_{e['dept_id']}", "WORKS_IN"))
    for ep in db_data['employee_projects']:
        expected_edges.append((f"emp_{ep['emp_id']}", f"proj_{ep['proj_id']}", "ASSIGNED_TO"))

    expected_edges.sort(key=lambda x: (x[0], x[1]))

    # Read actual nodes
    with open(GRAPH_NODES_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ['node_id', 'label', 'name'], f"Incorrect headers in {GRAPH_NODES_PATH}"
        actual_nodes = [tuple(row) for row in reader]
        actual_nodes.sort(key=lambda x: (x[0], x[1]))

    assert actual_nodes == expected_nodes, f"Nodes in {GRAPH_NODES_PATH} do not match expected output."

    # Read actual edges
    with open(GRAPH_EDGES_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ['source', 'target', 'relationship'], f"Incorrect headers in {GRAPH_EDGES_PATH}"
        actual_edges = [tuple(row) for row in reader]
        actual_edges.sort(key=lambda x: (x[0], x[1]))

    assert actual_edges == expected_edges, f"Edges in {GRAPH_EDGES_PATH} do not match expected output."