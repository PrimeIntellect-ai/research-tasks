# test_final_state.py

import os
import json
import sqlite3
import math
from collections import defaultdict

def get_age_group(age):
    if 18 <= age <= 25:
        return '18-25'
    elif 26 <= age <= 35:
        return '26-35'
    elif 36 <= age <= 50:
        return '36-50'
    elif age >= 51:
        return '51+'
    return 'unknown'

def compute_expected_report():
    events_dir = '/home/user/data/events'
    user_totals = defaultdict(float)

    # 1. Parse JSON session files and extract purchase events
    if os.path.exists(events_dir):
        for filename in os.listdir(events_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(events_dir, filename)
                with open(filepath, 'r') as f:
                    try:
                        data = json.load(f)
                        user_id = data.get('user_id')
                        events = data.get('events', [])
                        for ev in events:
                            if ev.get('type') == 'purchase':
                                user_totals[user_id] += float(ev.get('amount', 0.0))
                    except (json.JSONDecodeError, ValueError, TypeError):
                        continue

    # 2. Query users.db
    db_path = '/home/user/data/users.db'
    if not os.path.exists(db_path):
        return []

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, country, age, status FROM users WHERE status = 'active'")
    active_users = c.fetchall()
    conn.close()

    # 3. Aggregate into cohorts
    cohort_totals = defaultdict(float)
    cohort_counts = defaultdict(int)

    for user_id, country, age, status in active_users:
        if user_id in user_totals and user_totals[user_id] > 0:
            age_group = get_age_group(age)
            cohort_key = (country, age_group)
            cohort_totals[cohort_key] += user_totals[user_id]
            cohort_counts[cohort_key] += 1

    # 4. Calculate average total spend
    cohorts = []
    for cohort_key, total_spend in cohort_totals.items():
        country, age_group = cohort_key
        count = cohort_counts[cohort_key]
        avg_spend = round(total_spend / count, 2)
        cohorts.append({
            "country": country,
            "age_group": age_group,
            "avg_spend": avg_spend
        })

    # 5. Sort cohorts
    cohorts.sort(key=lambda x: (-x["avg_spend"], x["country"]))

    # 6. Limit to top 3
    return cohorts[:3]

def test_cohort_report_exists_and_correct():
    report_path = '/home/user/cohort_report.json'
    assert os.path.exists(report_path), f"The file {report_path} was not created."

    with open(report_path, 'r') as f:
        try:
            actual_report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    assert isinstance(actual_report, list), f"The content of {report_path} must be a JSON array."

    expected_report = compute_expected_report()

    assert len(actual_report) == len(expected_report), f"Expected {len(expected_report)} cohorts in the report, but found {len(actual_report)}."

    for i, (actual, expected) in enumerate(zip(actual_report, expected_report)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        assert set(actual.keys()) == {"country", "age_group", "avg_spend"}, f"Item at index {i} has incorrect keys. Expected exactly 'country', 'age_group', 'avg_spend'."
        assert actual["country"] == expected["country"], f"Cohort {i} 'country' mismatch: expected {expected['country']}, got {actual['country']}."
        assert actual["age_group"] == expected["age_group"], f"Cohort {i} 'age_group' mismatch: expected {expected['age_group']}, got {actual['age_group']}."
        assert math.isclose(actual["avg_spend"], expected["avg_spend"], rel_tol=1e-5), f"Cohort {i} 'avg_spend' mismatch: expected {expected['avg_spend']}, got {actual['avg_spend']}."