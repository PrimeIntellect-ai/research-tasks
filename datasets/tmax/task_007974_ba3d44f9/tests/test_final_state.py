# test_final_state.py
import os
import json
import subprocess
import pytest

def test_makefile_exists_and_runs():
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile does not exist at {makefile_path}"

    # Remove output file if it exists to ensure the make command recreates it
    output_file = "/home/user/output/processed.jsonl"
    if os.path.exists(output_file):
        os.remove(output_file)

    result = subprocess.run(["make", "-C", "/home/user", "all"], capture_output=True, text=True)
    assert result.returncode == 0, f"make command failed with error:\n{result.stderr}"

def test_output_file_exists():
    output_file = "/home/user/output/processed.jsonl"
    assert os.path.isfile(output_file), f"Output file does not exist at {output_file}"

def test_output_content():
    output_file = "/home/user/output/processed.jsonl"
    assert os.path.isfile(output_file), f"Output file does not exist at {output_file}"

    expected = [
        {"doc_id": "DOC_1", "category": "science", "tokens": ["the", "quick", "brown", "fox", "jumps", "over", "2", "lazy", "dogs"]},
        {"doc_id": "DOC_2", "category": "history", "tokens": ["history", "is", "written", "by", "the", "victors"]},
        {"doc_id": "DOC_3", "category": "art", "tokens": ["art", "is", "in", "the", "eye", "of", "the", "beholder"]}
    ]

    with open(output_file, "r") as f:
        data = [json.loads(line) for line in f if line.strip()]

    assert len(data) == 3, f"Expected 3 records, got {len(data)}"

    # Sort both to ensure order doesn't fail the test
    data.sort(key=lambda x: x.get("doc_id", ""))
    expected.sort(key=lambda x: x["doc_id"])

    assert data == expected, f"Data mismatch.\nExpected: {expected}\nGot: {data}"