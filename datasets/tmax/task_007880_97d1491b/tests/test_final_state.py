# test_final_state.py

import os
import csv
from collections import defaultdict

def test_suspects_csv_exists_and_correct():
    access_logs_path = "/home/user/access_logs.csv"
    employees_path = "/home/user/employees.csv"
    suspects_path = "/home/user/suspects.csv"

    assert os.path.exists(suspects_path), f"Output file {suspects_path} does not exist."
    assert os.path.isfile(suspects_path), f"{suspects_path} is not a file."

    # Compute expected output
    error_counts = defaultdict(int)
    with open(access_logs_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("status_code") == "403":
                error_counts[row.get("emp_id")] += 1

    suspect_ids = {emp_id: count for emp_id, count in error_counts.items() if count > 3}

    emp_emails = {}
    with open(employees_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_emails[row.get("emp_id")] = row.get("email")

    expected_rows = []
    for emp_id, count in suspect_ids.items():
        email = emp_emails.get(emp_id, "")
        if "@" in email:
            local, domain = email.split("@", 1)
            if len(local) > 0:
                masked_local = local[0] + "*" * (len(local) - 1)
            else:
                masked_local = local
            masked_email = f"{masked_local}@{domain}"
        else:
            masked_email = email

        expected_rows.append({
            "emp_id": emp_id,
            "masked_email": masked_email,
            "error_count": str(count)
        })

    expected_rows.sort(key=lambda x: x["emp_id"])

    # Read actual output
    with open(suspects_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            header = []

        assert header == ["emp_id", "masked_email", "error_count"], \
            f"Header in {suspects_path} is incorrect. Got: {header}"

        actual_rows = []
        for row in reader:
            if not row:
                continue
            assert len(row) == 3, f"Row in {suspects_path} does not have exactly 3 columns: {row}"
            actual_rows.append({
                "emp_id": row[0],
                "masked_email": row[1],
                "error_count": row[2]
            })

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in {suspects_path}, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, \
            f"Row {i+1} mismatch. Expected: {expected}, Got: {actual}"