# test_final_state.py
import os
import json
import csv
import pytest

def luhn_check(card_str):
    digits = [int(c) for c in card_str if c.isdigit()]
    if len(digits) != 16:
        return False

    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def mask_email(email):
    if "@" not in email:
        return email
    local, domain = email.split("@", 1)
    if not local:
        return email
    return f"{local[0]}***@{domain}"

def mask_card(card_str):
    chars = list(card_str)
    digit_count = 0
    total_digits = sum(1 for c in chars if c.isdigit())

    for i in range(len(chars)):
        if chars[i].isdigit():
            digit_count += 1
            if total_digits - digit_count >= 4:
                chars[i] = 'X'
    return "".join(chars)

def get_expected_data():
    raw_csv = "/home/user/raw_data/users.csv"
    raw_json = "/home/user/raw_data/users.json"

    records = []

    if os.path.exists(raw_csv):
        with open(raw_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "email": row["email"],
                    "age": int(row["age"]),
                    "card": row["card"]
                })

    if os.path.exists(raw_json):
        with open(raw_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            for row in data:
                records.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "email": row["email"],
                    "age": int(row["age"]),
                    "card": row["card"]
                })

    valid_records = []
    for r in records:
        if r["age"] >= 18 and luhn_check(r["card"]):
            masked_record = {
                "id": r["id"],
                "name": r["name"],
                "email": mask_email(r["email"]),
                "age": r["age"],
                "card": mask_card(r["card"])
            }
            valid_records.append(masked_record)

    valid_records.sort(key=lambda x: x["id"])
    return valid_records

def test_clean_data_directory():
    clean_dir = "/home/user/clean_data"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist."

    files = set(os.listdir(clean_dir))
    expected_files = {"unified.csv", "unified.json"}
    assert files == expected_files, f"Expected exactly {expected_files} in {clean_dir}, but found {files}. Intermediate files might have been left behind."

def test_unified_csv():
    csv_path = "/home/user/clean_data/unified.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    expected_data = get_expected_data()

    actual_data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["id", "name", "email", "age", "card"], "CSV header is incorrect."
        for row in reader:
            actual_data.append({
                "id": int(row["id"]),
                "name": row["name"],
                "email": row["email"],
                "age": int(row["age"]),
                "card": row["card"]
            })

    assert actual_data == expected_data, "The contents of unified.csv do not match the expected masked and filtered records."

def test_unified_json():
    json_path = "/home/user/clean_data/unified.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    expected_data = get_expected_data()

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("unified.json is not a valid JSON file.")

    assert isinstance(actual_data, list), "unified.json must contain a JSON array."

    # Ensure types are correct
    for row in actual_data:
        assert isinstance(row.get("id"), int), "ID in JSON must be an integer."
        assert isinstance(row.get("age"), int), "Age in JSON must be an integer."

    assert actual_data == expected_data, "The contents of unified.json do not match the expected masked and filtered records."