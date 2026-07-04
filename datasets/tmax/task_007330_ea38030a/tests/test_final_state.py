# test_final_state.py
import os
import json
import sqlite3

def test_denormalized_trials_json_exists():
    output_path = "/home/user/denormalized_trials.json"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_denormalized_trials_json_content():
    output_path = "/home/user/denormalized_trials.json"
    db_path = "/home/user/research_data.db"

    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    # Read student output
    try:
        with open(output_path, "r") as f:
            student_data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"{output_path} is not a valid JSON file."

    assert isinstance(student_data, list), f"Output JSON must be an array of objects."

    # Generate truth data from SQLite
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = """
        SELECT 
            t.id as trial_id, t.date, t.outcome, t.score,
            sub.id as subject_id, sub.age, sub.group_name as cohort_group,
            s.id as site_id, s.name as site_name, s.location as site_location
        FROM trials t
        JOIN subjects sub ON t.subject_id = sub.id
        JOIN sites s ON sub.site_id = s.id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        assert False, f"Failed to query database to generate truth data: {e}"

    expected_data = []
    for row in rows:
        expected_data.append({
            "trial_id": row["trial_id"],
            "date": row["date"],
            "outcome": row["outcome"],
            "score": row["score"],
            "subject": {
                "subject_id": row["subject_id"],
                "age": row["age"],
                "cohort_group": row["cohort_group"],
                "site": {
                    "site_id": row["site_id"],
                    "name": row["site_name"],
                    "location": row["site_location"]
                }
            }
        })

    # Sort both lists by trial_id to ensure order independence
    student_data_sorted = sorted(student_data, key=lambda x: x.get("trial_id", -1))
    expected_data_sorted = sorted(expected_data, key=lambda x: x["trial_id"])

    assert len(student_data_sorted) == len(expected_data_sorted), f"Expected {len(expected_data_sorted)} trials, found {len(student_data_sorted)}."

    for i, (student_item, expected_item) in enumerate(zip(student_data_sorted, expected_data_sorted)):
        assert student_item == expected_item, f"Mismatch at trial_id {expected_item['trial_id']}. Expected: {expected_item}, Got: {student_item}"