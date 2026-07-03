# test_final_state.py

import os
import csv
import math
import pytest

def test_script_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_output_file_exists():
    output_path = '/home/user/user_features.csv'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_output_content_matches_expected():
    output_path = '/home/user/user_features.csv'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    # Read inputs
    users = {}
    with open('/home/user/data/users.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row['user_id']] = {
                'total_net_spend': 0.0,
                'max_days_active': 1,
                'has_orders': False
            }

    returns = {}
    with open('/home/user/data/returns.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            returns[row['order_id']] = float(row['return_amount'])

    with open('/home/user/data/orders.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row['user_id']
            if user_id not in users:
                continue

            order_id = row['order_id']
            order_amount = float(row['order_amount'])
            days_active = int(row['days_active'])

            ret_amount = returns.get(order_id, 0.0)
            net_spend = order_amount - ret_amount

            users[user_id]['total_net_spend'] += net_spend
            if not users[user_id]['has_orders']:
                users[user_id]['max_days_active'] = days_active
                users[user_id]['has_orders'] = True
            else:
                if days_active > users[user_id]['max_days_active']:
                    users[user_id]['max_days_active'] = days_active

    expected_rows = []
    for user_id in sorted(users.keys(), key=lambda x: int(x)):
        u = users[user_id]
        tns = u['total_net_spend']
        mda = u['max_days_active']
        ltv = tns + (tns / mda) * 30
        ltv = round(ltv, 2)

        if ltv >= 500.00:
            segment = "VIP"
        elif ltv >= 100.00:
            segment = "Standard"
        else:
            segment = "Churn_Risk"

        expected_rows.append({
            'user_id': user_id,
            'total_net_spend': round(tns, 2),
            'max_days_active': mda,
            'predicted_LTV': ltv,
            'segment': segment
        })

    # Read actual
    actual_rows = []
    with open(output_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        expected_header = ['user_id', 'total_net_spend', 'max_days_active', 'predicted_LTV', 'segment']
        assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

        for row in reader:
            assert len(row) == 5, f"Row has incorrect number of columns: {row}"
            actual_rows.append({
                'user_id': row[0],
                'total_net_spend': float(row[1]),
                'max_days_active': int(float(row[2])),
                'predicted_LTV': float(row[3]),
                'segment': row[4]
            })

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(actual_rows)}"

    for i, (expected, actual) in enumerate(zip(expected_rows, actual_rows)):
        assert expected['user_id'] == actual['user_id'], f"Row {i}: user_id mismatch. Expected {expected['user_id']}, got {actual['user_id']}"
        assert math.isclose(expected['total_net_spend'], actual['total_net_spend'], abs_tol=0.01), f"Row {i}: total_net_spend mismatch for user {expected['user_id']}. Expected {expected['total_net_spend']}, got {actual['total_net_spend']}"
        assert expected['max_days_active'] == actual['max_days_active'], f"Row {i}: max_days_active mismatch for user {expected['user_id']}. Expected {expected['max_days_active']}, got {actual['max_days_active']}"
        assert math.isclose(expected['predicted_LTV'], actual['predicted_LTV'], abs_tol=0.01), f"Row {i}: predicted_LTV mismatch for user {expected['user_id']}. Expected {expected['predicted_LTV']}, got {actual['predicted_LTV']}"
        assert expected['segment'] == actual['segment'], f"Row {i}: segment mismatch for user {expected['user_id']}. Expected {expected['segment']}, got {actual['segment']}"