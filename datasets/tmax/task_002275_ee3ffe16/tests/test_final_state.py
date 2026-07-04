# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/ecommerce.db"
INSIGHTS_PATH = "/home/user/insights.json"

def get_expected_insights():
    """Compute the expected insights directly from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query to find users who purchased a product and gave it a 1-star review
    query = """
    SELECT DISTINCT p1.user_id, p1.product_id
    FROM purchases p1
    JOIN reviews r ON p1.user_id = r.user_id AND p1.product_id = r.product_id
    WHERE r.rating = 1
    """
    cursor.execute(query)
    bad_reviews = cursor.fetchall()

    target_products = set()
    for user_id, bad_product_id in bad_reviews:
        # Find other products purchased by the same user
        cursor.execute("""
        SELECT product_id 
        FROM purchases 
        WHERE user_id = ? AND product_id != ?
        """, (user_id, bad_product_id))

        other_products = cursor.fetchall()
        for (prod_id,) in other_products:
            target_products.add(prod_id)

    # Group target products by category
    expected_insights = {}
    for prod_id in target_products:
        cursor.execute("SELECT title, category FROM products WHERE id = ?", (prod_id,))
        title, category = cursor.fetchone()
        if category not in expected_insights:
            expected_insights[category] = []
        expected_insights[category].append(title)

    conn.close()

    # Sort the lists
    for category in expected_insights:
        expected_insights[category].sort()

    return expected_insights

def test_insights_file_exists():
    assert os.path.exists(INSIGHTS_PATH), f"Expected output file {INSIGHTS_PATH} does not exist."
    assert os.path.isfile(INSIGHTS_PATH), f"{INSIGHTS_PATH} is not a file."

def test_insights_content():
    assert os.path.exists(INSIGHTS_PATH), f"Cannot check content, {INSIGHTS_PATH} is missing."

    with open(INSIGHTS_PATH, 'r') as f:
        try:
            actual_insights = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{INSIGHTS_PATH} does not contain valid JSON.")

    expected_insights = get_expected_insights()

    # Check that the actual insights have exactly the expected keys
    assert set(actual_insights.keys()) == set(expected_insights.keys()), \
        f"Categories in insights.json {list(actual_insights.keys())} do not match expected {list(expected_insights.keys())}."

    # Check that the lists of titles match and are sorted
    for category, expected_titles in expected_insights.items():
        actual_titles = actual_insights[category]
        assert isinstance(actual_titles, list), f"Value for category '{category}' should be a list."
        assert actual_titles == expected_titles, \
            f"Titles for category '{category}' do not match expected. Expected: {expected_titles}, Actual: {actual_titles}."