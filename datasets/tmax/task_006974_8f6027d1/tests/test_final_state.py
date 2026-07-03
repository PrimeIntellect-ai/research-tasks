# test_final_state.py
import os
import sqlite3

def test_convert_binary_exists():
    """Check if the compiled C++ binary exists and is executable."""
    binary_path = "/home/user/convert"
    assert os.path.exists(binary_path), f"{binary_path} does not exist."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_import_cypher_exists_and_correct():
    """Check if the generated Cypher script exists and contains the correct commands."""
    cypher_path = "/home/user/import.cypher"
    assert os.path.exists(cypher_path), f"{cypher_path} does not exist."
    assert os.path.isfile(cypher_path), f"{cypher_path} is not a file."

    with open(cypher_path, "r") as f:
        actual_content = f.read().strip()

    db_path = "/home/user/hr_data.db"
    assert os.path.exists(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT emp_id, manager_id, salary, dept
    FROM (
        SELECT emp_id, manager_id, salary, dept,
               ROW_NUMBER() OVER(PARTITION BY emp_id ORDER BY event_timestamp DESC) as rn
        FROM emp_events
    ) tmp
    WHERE rn = 1
    ORDER BY emp_id ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    expected_blocks = []
    for emp_id, manager_id, salary, dept in rows:
        if manager_id == -1:
            continue

        salary_str = str(int(salary)) if salary == int(salary) else str(salary)

        block = (
            f"MERGE (e:Employee {{id: {emp_id}}}) SET e.salary = {salary_str}, e.dept = '{dept}';\n"
            f"MERGE (m:Employee {{id: {manager_id}}});\n"
            f"MERGE (e)-[:REPORTS_TO]->(m);"
        )
        expected_blocks.append(block)

    actual_blocks = [block.strip() for block in actual_content.split('\n\n') if block.strip()]

    assert len(actual_blocks) == len(expected_blocks), (
        f"Expected {len(expected_blocks)} employee blocks in the Cypher script, "
        f"but found {len(actual_blocks)}."
    )

    for i, (actual_block, expected_block) in enumerate(zip(actual_blocks, expected_blocks)):
        actual_lines = [line.strip() for line in actual_block.split('\n') if line.strip()]
        expected_lines = [line.strip() for line in expected_block.split('\n') if line.strip()]

        assert actual_lines == expected_lines, (
            f"Employee block {i+1} does not match expected output.\n"
            f"Expected:\n{expected_block}\n\n"
            f"Actual:\n{actual_block}"
        )