# test_final_state.py
import os
import csv
import json
import pytest

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def mask_ip(ip):
    parts = ip.split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.*.*"
    return ip

def mask_email(email):
    if '@' in email:
        user, domain = email.split('@', 1)
        if len(user) > 0:
            return f"{user[0]}****@{domain}"
    return email

def get_expected_results():
    web_logs_path = '/home/user/web_logs.csv'
    db_logs_path = '/home/user/db_logs.csv'

    web_extracted = []
    status_counts = {}

    with open(web_logs_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = row['status_code']
            if status_counts.get(status, 0) < 20:
                web_extracted.append(row)
                status_counts[status] = status_counts.get(status, 0) + 1

    db_logs = {}
    with open(db_logs_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            req_id = row['req_id']
            if req_id not in db_logs:
                db_logs[req_id] = []
            db_logs[req_id].append(row)

    results = []
    for web_row in web_extracted:
        req_id = web_row['req_id']
        if req_id in db_logs:
            min_dist = float('inf')
            best_db_row = None
            for db_row in db_logs[req_id]:
                dist = levenshtein(web_row['error_msg'], db_row['db_error'])
                if dist < min_dist:
                    min_dist = dist
                    best_db_row = db_row

            if min_dist < 15 and best_db_row is not None:
                results.append({
                    "req_id": req_id,
                    "status_code": int(web_row['status_code']) if web_row['status_code'].isdigit() else web_row['status_code'],
                    "masked_ip": mask_ip(web_row['ip_address']),
                    "masked_email": mask_email(best_db_row['user_email']),
                    "web_error": web_row['error_msg'],
                    "db_error": best_db_row['db_error'],
                    "edit_distance": min_dist
                })

    results.sort(key=lambda x: x['req_id'])
    return results

def test_investigation_results_exists():
    file_path = '/home/user/investigation_results.jsonl'
    assert os.path.exists(file_path), f"Output file {file_path} was not created."
    assert os.path.isfile(file_path), f"Output path {file_path} is not a file."

def test_investigation_results_content():
    file_path = '/home/user/investigation_results.jsonl'
    assert os.path.exists(file_path), f"Output file {file_path} was not created."

    expected = get_expected_results()
    actual = []

    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                # Cast status_code to int if it's a string representing an int, to be robust
                if 'status_code' in obj and isinstance(obj['status_code'], str) and obj['status_code'].isdigit():
                    obj['status_code'] = int(obj['status_code'])
                actual.append(obj)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {file_path} is not valid JSON.")

    assert len(actual) == len(expected), f"Expected {len(expected)} results, but got {len(actual)}."

    for i, (act, exp) in enumerate(zip(actual, expected)):
        assert act.get('req_id') == exp['req_id'], f"Row {i} req_id mismatch: expected {exp['req_id']}, got {act.get('req_id')}. Ensure sorting by req_id."
        assert act == exp, f"Row {i} mismatch. Expected: {exp}, Got: {act}"