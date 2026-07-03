# test_final_state.py
import os
import subprocess
import json

def test_script_exists_and_executable():
    script_path = '/home/user/generate_report.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def run_script_and_parse_json(category, page):
    script_path = '/home/user/generate_report.sh'
    result = subprocess.run([script_path, category, str(page)], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, f"Script output is not valid JSON. Output: {result.stdout}"

    return data

def test_clothing_page_2():
    data = run_script_and_parse_json("Clothing", 2)

    assert data.get("category") == "Clothing", "Expected category 'Clothing'."
    assert data.get("page") == 2, "Expected page 2."

    results = data.get("results", [])
    assert len(results) == 2, f"Expected exactly 2 results on page 2, got {len(results)}."

    assert results[0] == {
        "rank": 3,
        "product_id": 5,
        "name": "Shirt",
        "total_revenue": 200
    }, f"First result on page 2 is incorrect. Got: {results[0]}"

    assert results[1] == {
        "rank": 3,
        "product_id": 7,
        "name": "Jacket",
        "total_revenue": 200
    }, f"Second result on page 2 is incorrect. Got: {results[1]}"

def test_electronics_page_1():
    data = run_script_and_parse_json("Electronics", 1)

    assert data.get("category") == "Electronics", "Expected category 'Electronics'."
    assert data.get("page") == 1, "Expected page 1."

    results = data.get("results", [])
    assert len(results) == 2, f"Expected exactly 2 results on page 1, got {len(results)}."

    assert results[0] == {
        "rank": 1,
        "product_id": 1,
        "name": "Laptop",
        "total_revenue": 4000
    }, f"First result on page 1 is incorrect. Got: {results[0]}"

    assert results[1] == {
        "rank": 2,
        "product_id": 2,
        "name": "Smartphone",
        "total_revenue": 3500
    }, f"Second result on page 1 is incorrect. Got: {results[1]}"

def test_clothing_page_3():
    data = run_script_and_parse_json("Clothing", 3)

    assert data.get("category") == "Clothing", "Expected category 'Clothing'."
    assert data.get("page") == 3, "Expected page 3."

    results = data.get("results", [])
    assert len(results) == 2, f"Expected exactly 2 results on page 3, got {len(results)}."

    assert results[0] == {
        "rank": 3,
        "product_id": 8,
        "name": "Hat",
        "total_revenue": 200
    }, f"First result on page 3 is incorrect. Got: {results[0]}"

    assert results[1] == {
        "rank": 6,
        "product_id": 9,
        "name": "Socks",
        "total_revenue": 150
    }, f"Second result on page 3 is incorrect. Got: {results[1]}"