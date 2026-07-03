# test_final_state.py
import os
import csv
import subprocess
import tempfile
import pytest

def test_classifier_exists():
    assert os.path.exists("/home/user/classifier.py"), "classifier.py not found at /home/user/classifier.py"

def test_classifier_clean_corpus():
    script_path = "/home/user/classifier.py"
    input_dir = "/app/corpus/clean"

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        output_csv = tmp.name

    try:
        result = subprocess.run(
            ["python3", script_path, input_dir, output_csv],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"Script failed on clean corpus: {result.stderr}"
        assert os.path.exists(output_csv), "Output CSV was not created for clean corpus."

        results = {}
        with open(output_csv, 'r', newline='') as f:
            reader = csv.DictReader(f)
            assert 'filename' in reader.fieldnames and 'status' in reader.fieldnames, "Output CSV must contain 'filename' and 'status' columns."
            for row in reader:
                results[row['filename']] = row['status']

        expected_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

        failed_files = []
        for f in expected_files:
            if f not in results:
                failed_files.append(f"{f} (missing)")
            elif results[f] != "clean":
                failed_files.append(f"{f} (status: {results[f]})")

        assert not failed_files, f"{len(failed_files)} of {len(expected_files)} clean files modified/flagged incorrectly: {', '.join(failed_files)}"

    finally:
        if os.path.exists(output_csv):
            os.remove(output_csv)


def test_classifier_evil_corpus():
    script_path = "/home/user/classifier.py"
    input_dir = "/app/corpus/evil"

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        output_csv = tmp.name

    try:
        result = subprocess.run(
            ["python3", script_path, input_dir, output_csv],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"Script failed on evil corpus: {result.stderr}"
        assert os.path.exists(output_csv), "Output CSV was not created for evil corpus."

        results = {}
        with open(output_csv, 'r', newline='') as f:
            reader = csv.DictReader(f)
            assert 'filename' in reader.fieldnames and 'status' in reader.fieldnames, "Output CSV must contain 'filename' and 'status' columns."
            for row in reader:
                results[row['filename']] = row['status']

        expected_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

        failed_files = []
        for f in expected_files:
            if f not in results:
                failed_files.append(f"{f} (missing)")
            elif results[f] != "evil":
                failed_files.append(f"{f} (status: {results[f]})")

        assert not failed_files, f"{len(failed_files)} of {len(expected_files)} evil files bypassed/flagged incorrectly: {', '.join(failed_files)}"

    finally:
        if os.path.exists(output_csv):
            os.remove(output_csv)