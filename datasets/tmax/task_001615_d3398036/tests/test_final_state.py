# test_final_state.py

import os
import csv
import json
import pytest

def get_expected_data():
    csv_path = "/home/user/pipeline_logs.csv"
    if not os.path.exists(csv_path):
        pytest.fail(f"Input file {csv_path} is missing.")

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    valid_rows = []
    for r in rows:
        if int(r["RowsProcessed"]) != 0:
            valid_rows.append(r)

    pipelines = {}
    for r in valid_rows:
        pid = r["PipelineID"]
        if pid not in pipelines:
            pipelines[pid] = []
        pipelines[pid].append({
            "task_id": r["TaskID"],
            "duration_sec": int(r["DurationSec"]),
            "rows_processed": int(r["RowsProcessed"])
        })

    expected = []
    for pid in sorted(pipelines.keys()):
        tasks = pipelines[pid]
        tasks.sort(key=lambda x: (-x["duration_sec"], x["task_id"]))
        top_tasks = tasks[:2]

        top_tasks_output = []
        total_rows = 0
        for i, t in enumerate(top_tasks):
            top_tasks_output.append({
                "task_id": t["task_id"],
                "rank": i + 1,
                "duration_sec": t["duration_sec"]
            })
            total_rows += t["rows_processed"]

        expected.append({
            "pipeline_id": pid,
            "top_tasks": top_tasks_output,
            "top_2_rows_processed": total_rows
        })

    return expected

def test_etl_summary_json_exists():
    file_path = "/home/user/etl_summary.json"
    assert os.path.exists(file_path), f"The file {file_path} was not created."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_etl_summary_json_content():
    file_path = "/home/user/etl_summary.json"
    assert os.path.exists(file_path), f"The file {file_path} was not created."

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        actual_data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_data = get_expected_data()

    assert actual_data == expected_data, (
        f"The parsed JSON content in {file_path} does not match the expected output. "
        f"Expected: {expected_data}\nActual: {actual_data}"
    )

def test_etl_summary_json_formatting():
    file_path = "/home/user/etl_summary.json"
    assert os.path.exists(file_path), f"The file {file_path} was not created."

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if the file is pretty-printed (contains newlines and indentation)
    assert "\n" in content, "The JSON output does not appear to be pretty-printed (missing newlines)."
    assert "  " in content, "The JSON output does not appear to use 2 spaces for indentation."