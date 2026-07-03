# test_final_state.py
import os
import json

def test_sqlite3_dev_installed():
    """Check if libsqlite3-dev is installed."""
    assert os.path.isfile("/usr/include/sqlite3.h"), "libsqlite3-dev is not installed (sqlite3.h missing)."

def test_c_source_exists_and_uses_json():
    """Check if the C source file exists and uses json_object."""
    c_file = "/home/user/workspace/analyze_bom.c"
    assert os.path.isfile(c_file), f"{c_file} is missing."
    with open(c_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    assert "json_object" in content, "The C source code does not appear to use SQLite's json_object function."

def test_executable_exists():
    """Check if the compiled executable exists."""
    exe_file = "/home/user/workspace/analyze_bom"
    assert os.path.isfile(exe_file), f"{exe_file} is missing."
    assert os.access(exe_file, os.X_OK), f"{exe_file} is not executable."

def test_query_plan():
    """Check if the query plan file exists and indicates index usage."""
    plan_file = "/home/user/workspace/query_plan.txt"
    assert os.path.isfile(plan_file), f"{plan_file} is missing."
    with open(plan_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().upper()
    assert "USING INDEX" in content or "USING COVERING INDEX" in content, \
        "query_plan.txt does not indicate that an index was used."

def test_bom_result():
    """Check if the JSON result file exists and contains the correct calculated cost."""
    json_file = "/home/user/workspace/bom_result.json"
    assert os.path.isfile(json_file), f"{json_file} is missing."
    with open(json_file, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        assert False, f"{json_file} does not contain valid JSON."

    assert "top_part_id" in data, "JSON result is missing 'top_part_id'."
    assert data["top_part_id"] == 1, f"Expected top_part_id to be 1, got {data['top_part_id']}."

    assert "total_assembly_cost" in data, "JSON result is missing 'total_assembly_cost'."
    cost = float(data["total_assembly_cost"])
    assert abs(cost - 70.0) < 1e-5, f"Expected total_assembly_cost to be 70.0, got {cost}."