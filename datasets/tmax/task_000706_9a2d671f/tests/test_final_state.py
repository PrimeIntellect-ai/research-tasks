# test_final_state.py
import sqlite3
import requests
import pytest

def get_expected_employees(db_path, start_dept_id, exclude_dept_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    WITH RECURSIVE dept_tree AS (
        SELECT id FROM departments WHERE id = ? AND id != ?
        UNION ALL
        SELECT d.id FROM departments d
        INNER JOIN dept_tree t ON d.parent_id = t.id
        WHERE d.id != ?
    )
    SELECT e.name FROM employees e
    INNER JOIN dept_tree t ON e.dept_id = t.id
    ORDER BY e.name ASC
    """
    cursor.execute(query, (start_dept_id, exclude_dept_id, exclude_dept_id))
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def test_indexes_created():
    conn = sqlite3.connect('/app/company.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    indexes = cursor.fetchall()
    conn.close()
    assert len(indexes) > 0, "No indexes were created to optimize the query. You must create necessary indexes."

def test_api_hierarchy():
    expected = get_expected_employees('/app/company.db', 1, 854)

    try:
        response = requests.get("http://127.0.0.1:8080/hierarchy?dept_id=1", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API at 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"API response is not valid JSON. Response text: {response.text}")

    assert isinstance(data, list), f"API response must be a JSON array, got {type(data)}"

    # Check if lengths match first for a better error message if it's completely off
    assert len(data) == len(expected), f"Expected {len(expected)} employees, but got {len(data)}. Ensure you are excluding the department correctly."

    # Check exact match
    assert data == expected, "API returned incorrect employee hierarchy or incorrect sorting."