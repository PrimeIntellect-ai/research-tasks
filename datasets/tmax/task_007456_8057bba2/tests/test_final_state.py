# test_final_state.py

import os
import json
import csv
import pytest

def test_cypher_queries_jsonl():
    csv_path = "/home/user/suspicious.csv"
    jsonl_path = "/home/user/cypher_queries.jsonl"

    assert os.path.isfile(jsonl_path), f"Output file {jsonl_path} is missing. Ensure your C program writes to this path."

    expected_objects = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entity_id = row["entity_id"]
            expected_objects.append({
                "statement": "MATCH path=(e:Entity {id: $entity_id})-[:TRANSFERRED*1..4]->(e) RETURN path",
                "parameters": {"entity_id": entity_id}
            })

    actual_objects = []
    with open(jsonl_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    actual_objects.append(json.loads(line))
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON line in {jsonl_path}: {line}")

    assert actual_objects == expected_objects, f"Contents of {jsonl_path} do not match the expected output based on the entities in {csv_path}."

def test_audit_report_json():
    input_jsonl = "/home/user/graph_results.jsonl"
    output_json = "/home/user/audit_report.json"

    assert os.path.isfile(output_json), f"Output file {output_json} is missing. Ensure your bash script writes to this path."

    expected_report = []
    with open(input_jsonl, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                entity_id = data["entity_id"]
                cycle_lengths = data.get("cycle_lengths", [])
                total_cycles = len(cycle_lengths)
                max_cycle_length = max(cycle_lengths) if total_cycles > 0 else None

                expected_report.append({
                    "entity_id": entity_id,
                    "total_cycles": total_cycles,
                    "max_cycle_length": max_cycle_length
                })

    with open(output_json, "r") as f:
        try:
            actual_report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_json} does not contain valid JSON.")

    assert actual_report == expected_report, f"Contents of {output_json} do not match the expected aggregated report. Check your jq aggregation logic."