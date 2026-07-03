# test_final_state.py
import os
import sqlite3
import gzip
import json
import pytest

DB_PATH = '/home/user/ecommerce.db'
REPORT_PATH = '/home/user/cohort_report.jsonl.gz'

def test_indexes_created():
    """Verify that the student created indexes on foreign keys and date columns."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = c.fetchall()
    conn.close()

    assert len(indexes) > 0, "No custom indexes were created in the database."

    # We expect indexes on foreign keys and/or date columns.
    # Just checking that at least one index exists on the relevant tables.
    indexed_tables = {row[1] for row in indexes}
    expected_tables_to_index = {'orders', 'order_items', 'customers'}
    assert len(indexed_tables.intersection(expected_tables_to_index)) > 0, \
        "Indexes should be created on tables involved in joins or date filtering (orders, order_items, customers)."

def test_report_exists_and_is_gzipped():
    """Verify the report file exists and is a valid gzip file."""
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    try:
        with gzip.open(REPORT_PATH, 'rt') as f:
            f.read(1)
    except Exception as e:
        pytest.fail(f"{REPORT_PATH} is not a valid gzip file: {e}")

def test_report_contents():
    """Verify the contents of the report match the database truth."""
    # Compute the expected results from the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Calculate expected total_clv per cohort
    c.execute("""
        SELECT strftime('%Y-%m', c.joined_date) AS cohort, SUM(o.total_amount)
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        GROUP BY cohort
        ORDER BY cohort
    """)
    expected_clv = {row[0]: round(row[1], 2) for row in c.fetchall()}

    # Calculate expected top categories per cohort
    c.execute("""
        SELECT strftime('%Y-%m', c.joined_date) AS cohort, p.category, SUM(oi.quantity * oi.price) as revenue
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        GROUP BY cohort, p.category
    """)

    cohort_categories = {}
    for row in c.fetchall():
        cohort, category, revenue = row
        if cohort not in cohort_categories:
            cohort_categories[cohort] = []
        cohort_categories[cohort].append({"category": category, "revenue": round(revenue, 2)})

    expected_cohorts = []
    for cohort in sorted(expected_clv.keys()):
        # Sort categories by revenue descending, then take top 2
        sorted_cats = sorted(cohort_categories.get(cohort, []), key=lambda x: x['revenue'], reverse=True)[:2]
        expected_cohorts.append({
            "cohort": cohort,
            "total_clv": expected_clv[cohort],
            "top_categories": sorted_cats
        })
    conn.close()

    # Read the actual results
    actual_cohorts = []
    with gzip.open(REPORT_PATH, 'rt') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                actual_cohorts.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {REPORT_PATH} is not valid JSON.")

    # Verify the structure and contents
    assert len(actual_cohorts) == len(expected_cohorts), \
        f"Expected {len(expected_cohorts)} cohorts, but found {len(actual_cohorts)}."

    for i, (actual, expected) in enumerate(zip(actual_cohorts, expected_cohorts)):
        assert actual.get("cohort") == expected["cohort"], \
            f"Row {i}: Expected cohort '{expected['cohort']}', got '{actual.get('cohort')}'."

        assert "total_clv" in actual, f"Row {i}: Missing 'total_clv'."
        assert round(actual["total_clv"], 2) == expected["total_clv"], \
            f"Row {i}: Expected total_clv {expected['total_clv']}, got {actual['total_clv']}."

        assert "top_categories" in actual, f"Row {i}: Missing 'top_categories'."
        actual_cats = actual["top_categories"]
        expected_cats = expected["top_categories"]

        assert len(actual_cats) == len(expected_cats), \
            f"Row {i}: Expected {len(expected_cats)} top categories, got {len(actual_cats)}."

        for j, (a_cat, e_cat) in enumerate(zip(actual_cats, expected_cats)):
            assert a_cat.get("category") == e_cat["category"], \
                f"Row {i}, Category {j}: Expected '{e_cat['category']}', got '{a_cat.get('category')}'."
            assert round(a_cat.get("revenue", 0), 2) == e_cat["revenue"], \
                f"Row {i}, Category {j}: Expected revenue {e_cat['revenue']}, got {a_cat.get('revenue')}."