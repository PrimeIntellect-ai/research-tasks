# test_final_state.py

import os
import json
import pytest

REPORT_PATH = '/home/user/top_customers_report.json'

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"Report file missing at {REPORT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file"

def test_report_structure_and_data():
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON")

    assert isinstance(data, list), "Top level JSON structure must be a list"
    assert len(data) == 5, f"Expected exactly 5 customers in the report, found {len(data)}"

    # Check sorting by spend_rank ascending
    ranks = [c.get('spend_rank') for c in data]
    assert ranks == sorted(ranks), "Customers are not sorted by spend_rank ascending"

    # Define expected data logic
    expected_spends = {
        2: {'name': 'Bob', 'segment': 'Enterprise', 'spend': 3500.0, 'rank': 1},
        1: {'name': 'Alice', 'segment': 'Retail', 'spend': 1000.0, 'rank': 2},
        6: {'name': 'Frank', 'segment': 'Enterprise', 'spend': 1000.0, 'rank': 2},
        4: {'name': 'Diana', 'segment': 'Enterprise', 'spend': 900.0, 'rank': 4},
        3: {'name': 'Charlie', 'segment': 'Retail', 'spend': 100.0, 'rank': 5},
    }

    expected_categories = {
        2: [('Electronics', 2500.0), ('Home', 1000.0)],
        1: [('Home', 1000.0)],
        6: [('Electronics', 1000.0)],
        4: [('Books', 500.0), ('Clothing', 400.0)],
        3: [('Books', 100.0)],
    }

    for item in data:
        cid = item.get('customer_id')
        assert cid in expected_spends, f"Unexpected customer_id {cid} in report"

        expected = expected_spends[cid]
        assert item.get('customer_name') == expected['name'], f"Incorrect name for customer {cid}"
        assert item.get('segment') == expected['segment'], f"Incorrect segment for customer {cid}"
        assert float(item.get('lifetime_spend')) == expected['spend'], f"Incorrect lifetime_spend for customer {cid}"

        # Rank can be checked strictly
        assert item.get('spend_rank') == expected['rank'], f"Incorrect spend_rank for customer {cid}"

        top_cats = item.get('top_categories', [])
        assert isinstance(top_cats, list), f"top_categories for customer {cid} must be a list"

        # Check sorting of top_categories descending by category_spend
        cat_spends = [c.get('category_spend') for c in top_cats]
        assert cat_spends == sorted(cat_spends, reverse=True), f"top_categories for customer {cid} not sorted by category_spend descending"

        exp_cats = expected_categories[cid]
        assert len(top_cats) == len(exp_cats), f"Incorrect number of categories for customer {cid}"

        for act_cat, exp_cat in zip(top_cats, exp_cats):
            assert act_cat.get('category_name') == exp_cat[0], f"Incorrect category_name for customer {cid}"
            assert float(act_cat.get('category_spend')) == exp_cat[1], f"Incorrect category_spend for customer {cid}"