# test_final_state.py

import os
import subprocess
import sqlite3
import ctypes
import re
import pytest

def test_stage1_libfastcalc_built():
    so_path = "/app/fast-calc-2.1.0/libfastcalc.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} is missing. Make sure the Makefile was fixed and executed."

    try:
        lib = ctypes.CDLL(so_path)
    except Exception as e:
        pytest.fail(f"Failed to load {so_path}. It might not be properly compiled or linked: {e}")

def test_stage2_sanitizer_executable():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer executable {sanitizer_path} is missing."
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer {sanitizer_path} is not executable."

def run_sanitizer(expr):
    sanitizer_path = "/home/user/sanitizer"
    result = subprocess.run([sanitizer_path, expr], capture_output=True, text=True)
    return result.stdout.strip()

def test_stage2_adversarial_corpus():
    evil_path = "/app/corpora/evil/evil_expr.txt"
    clean_path = "/app/corpora/clean/clean_expr.txt"

    assert os.path.isfile(evil_path), f"Missing evil corpus at {evil_path}"
    assert os.path.isfile(clean_path), f"Missing clean corpus at {clean_path}"

    with open(evil_path, "r") as f:
        evil_exprs = [line.strip() for line in f if line.strip()]

    with open(clean_path, "r") as f:
        clean_exprs = [line.strip() for line in f if line.strip()]

    evil_bypassed = []
    for expr in evil_exprs:
        if run_sanitizer(expr) != "REJECT":
            evil_bypassed.append(expr)

    clean_modified = []
    for expr in clean_exprs:
        if run_sanitizer(expr) != "ACCEPT":
            clean_modified.append(expr)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_exprs)} evil bypassed: {evil_bypassed[:5]}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_exprs)} clean modified/rejected: {clean_modified[:5]}")

    if errors:
        pytest.fail(" | ".join(errors))

def python_is_valid(expr):
    depth = 0
    for char in expr:
        if char == '(':
            depth += 1
            if depth > 5:
                return False
        elif char == ')':
            depth -= 1

    if any(c in expr for c in '%&|^'):
        return False

    if re.search(r'/\s*0+(\.0+)?\b', expr):
        return False

    return True

def test_stage3_schema_migration():
    db_path = "/home/user/math_data.db"
    assert os.path.isfile(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='equations_v2';")
    assert cursor.fetchone() is not None, "Table 'equations_v2' does not exist."

    cursor.execute("SELECT id, expression FROM equations_v1;")
    v1_rows = cursor.fetchall()

    cursor.execute("SELECT id, expression, status FROM equations_v2;")
    v2_rows = cursor.fetchall()

    conn.close()

    assert len(v2_rows) == len(v1_rows), f"Expected {len(v1_rows)} rows in equations_v2, got {len(v2_rows)}."

    v2_dict = {row[0]: (row[1], row[2]) for row in v2_rows}

    wrong_status = []
    for id_val, expr in v1_rows:
        assert id_val in v2_dict, f"Row with id {id_val} missing in equations_v2."
        v2_expr, v2_status = v2_dict[id_val]
        assert expr == v2_expr, f"Expression for id {id_val} was altered."

        expected_status = "VALID" if python_is_valid(expr) else "INVALID"
        if v2_status != expected_status:
            wrong_status.append(id_val)

    if wrong_status:
        pytest.fail(f"Incorrect status for {len(wrong_status)} rows in equations_v2. Example IDs: {wrong_status[:5]}")