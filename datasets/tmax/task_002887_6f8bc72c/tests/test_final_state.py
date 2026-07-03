# test_final_state.py

import os
import json
import subprocess
import pytest
import csv

def test_filter_clean_corpus():
    clean_dir = "/app/corpora/clean"
    expected_ids = set()
    for fname in os.listdir(clean_dir):
        if fname.endswith('.json'):
            with open(os.path.join(clean_dir, fname)) as f:
                try:
                    data = json.load(f)
                    expected_ids.add(data.get("id"))
                except json.JSONDecodeError:
                    pass

    result = subprocess.run(["python3", "/home/user/filter.py", clean_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"filter.py failed on clean corpus: {result.stderr}"

    try:
        output_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail("filter.py did not output valid JSON on clean corpus.")

    output_ids = {item.get("id") for item in output_data if isinstance(item, dict)}

    missing = expected_ids - output_ids
    if missing:
        pytest.fail(f"{len(missing)} of {len(expected_ids)} clean modified/rejected. Missing IDs: {missing}")

def test_filter_evil_corpus():
    evil_dir = "/app/corpora/evil"
    expected_ids = set()
    for fname in os.listdir(evil_dir):
        if fname.endswith('.json'):
            with open(os.path.join(evil_dir, fname)) as f:
                try:
                    data = json.load(f)
                    expected_ids.add(data.get("id"))
                except json.JSONDecodeError:
                    pass

    result = subprocess.run(["python3", "/home/user/filter.py", evil_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"filter.py failed on evil corpus: {result.stderr}"

    try:
        output_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail("filter.py did not output valid JSON on evil corpus.")

    output_ids = {item.get("id") for item in output_data if isinstance(item, dict)}

    bypassed = expected_ids.intersection(output_ids)
    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(expected_ids)} evil bypassed. Bypassed IDs: {bypassed}")

def test_final_report_exists_and_format():
    report_path = "/home/user/final_report.csv"
    assert os.path.isfile(report_path), f"Final report not found at {report_path}"

    with open(report_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["id", "user_name", "department", "final_metric"], "Incorrect CSV header in final report."

        rows = list(reader)
        assert len(rows) > 0, "Final report CSV is empty."

        # Check sorting
        ids = [row[0] for row in rows]
        assert ids == sorted(ids), "Final report CSV is not sorted alphanumerically by id."