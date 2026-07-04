# test_final_state.py
import os
import csv
import re
import pytest

OUTPUT_PATH = "/home/user/clean_long_survey.csv"
METADATA_PATH = "/home/user/metadata.csv"
SURVEY_DIR = "/home/user/survey_data"
SURVEY_FILES = ["survey_NA.csv", "survey_EU.csv", "survey_APAC.csv"]

def is_valid_emp_id(emp_id):
    return bool(re.match(r"^EMP\d{5}$", emp_id))

def is_valid_score(score_str):
    try:
        score = int(score_str)
        return 1 <= score <= 10
    except ValueError:
        return False

def get_expected_data():
    # Read metadata
    metadata = {}
    with open(METADATA_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metadata[row["emp_id"]] = {
                "hire_year": row["hire_year"],
                "office_city": row["office_city"]
            }

    # Read and process survey data
    expected_rows = []
    questions = ["q1_satisfaction", "q2_workload", "q3_culture", "q4_management"]

    for filename in SURVEY_FILES:
        filepath = os.path.join(SURVEY_DIR, filename)
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                emp_id = row["emp_id"]
                if not is_valid_emp_id(emp_id):
                    continue

                valid_scores = True
                for q in questions:
                    if not is_valid_score(row[q]):
                        valid_scores = False
                        break

                if not valid_scores:
                    continue

                if emp_id not in metadata:
                    continue

                for q in questions:
                    expected_rows.append({
                        "emp_id": emp_id,
                        "hire_year": metadata[emp_id]["hire_year"],
                        "office_city": metadata[emp_id]["office_city"],
                        "question": q,
                        "score": str(int(row[q]))
                    })

    # Sort expected rows
    expected_rows.sort(key=lambda x: (x["emp_id"], x["question"]))
    return expected_rows

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_PATH), f"The output file {OUTPUT_PATH} does not exist."

def test_output_file_header():
    with open(OUTPUT_PATH, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
    expected_header = ["emp_id", "hire_year", "office_city", "question", "score"]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}"

def test_output_file_contents_and_sorting():
    expected_data = get_expected_data()

    actual_data = []
    with open(OUTPUT_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            actual_data.append(row)

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows, but got {len(actual_data)} rows."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, but got {actual}. Check sorting and data validation."