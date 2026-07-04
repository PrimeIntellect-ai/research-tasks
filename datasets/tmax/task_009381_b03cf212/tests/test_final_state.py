# test_final_state.py

import os
import json
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_data.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_report_json_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file not found at {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON")

    assert isinstance(data, list), "Root JSON element should be a list"
    assert len(data) == 2, f"Expected exactly 2 categories, found {len(data)}"

    # Check first category (Clothing)
    cat1 = data[0]
    assert cat1.get("category") == "Clothing", f"Expected first category to be 'Clothing', got {cat1.get('category')}"

    top_products_1 = cat1.get("top_products", [])
    assert len(top_products_1) == 2, "Expected 2 top products for Clothing"

    assert top_products_1[0].get("rank") == 1
    assert top_products_1[0].get("product_name") == "Jacket"
    assert float(top_products_1[0].get("total_amount")) == 100.0

    assert top_products_1[1].get("rank") == 2
    assert top_products_1[1].get("product_name") == "Jeans"
    assert float(top_products_1[1].get("total_amount")) == 100.0

    # Check second category (Electronics)
    cat2 = data[1]
    assert cat2.get("category") == "Electronics", f"Expected second category to be 'Electronics', got {cat2.get('category')}"

    top_products_2 = cat2.get("top_products", [])
    assert len(top_products_2) == 2, "Expected 2 top products for Electronics"

    assert top_products_2[0].get("rank") == 1
    assert top_products_2[0].get("product_name") == "Laptop"
    assert float(top_products_2[0].get("total_amount")) == 2000.0

    assert top_products_2[1].get("rank") == 2
    assert top_products_2[1].get("product_name") == "Smartphone"
    assert float(top_products_2[1].get("total_amount")) == 1600.0