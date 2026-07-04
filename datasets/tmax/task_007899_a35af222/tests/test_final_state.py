# test_final_state.py

import os
import re
import csv
import math
import pytest
import subprocess
import tempfile

def test_venv_exists():
    assert os.path.exists("/home/user/venv/bin/python"), "Virtual environment python binary not found at /home/user/venv/bin/python"

def test_script_exists():
    assert os.path.exists("/home/user/process_alignments.py"), "Processing script not found at /home/user/process_alignments.py"

def test_results_csv_exists_and_format():
    csv_path = "/home/user/results.csv"
    assert os.path.exists(csv_path), "results.csv missing"

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ["sequence_id", "gc_content", "alignment_score"], "results.csv headers are incorrect"

        rows = list(reader)
        assert len(rows) > 0, "results.csv is empty"
        for row in rows:
            assert len(row) == 3, f"Row {row} does not have exactly 3 columns"
            # verify floats
            try:
                float(row[1])
                float(row[2])
            except ValueError:
                pytest.fail(f"Could not parse gc_content or alignment_score as float in row: {row}")

def test_model_stats_and_correctness():
    stats_path = "/home/user/model_stats.txt"
    assert os.path.exists(stats_path), "model_stats.txt missing"

    with open(stats_path, "r") as f:
        content = f.read()

    slope_match = re.search(r"Slope:\s*(-?\d+\.\d{4})", content)
    intercept_match = re.search(r"Intercept:\s*(-?\d+\.\d{4})", content)

    assert slope_match, "model_stats.txt does not contain correctly formatted Slope"
    assert intercept_match, "model_stats.txt does not contain correctly formatted Intercept"

    actual_slope = float(slope_match.group(1))
    actual_intercept = float(intercept_match.group(1))

    # Generate expected values using the user's venv
    script = """
import sys
try:
    from Bio import Align
    from Bio.SeqUtils import gc_fraction
    from sklearn.linear_model import LinearRegression
    import numpy as np
except ImportError:
    sys.exit(1)

primer = "CGTAGCTAGCC"
aligner = Align.PairwiseAligner()
aligner.mode = 'local'
aligner.match_score = 2
aligner.mismatch_score = -1
aligner.open_gap_score = -2
aligner.extend_gap_score = -0.5

X = []
y = []

with open("/home/user/genomics_data/sequences.fasta", "r") as f:
    lines = f.readlines()

seqs = []
curr = []
for line in lines:
    if line.startswith(">"):
        if curr:
            seqs.append("".join(curr))
            curr = []
    else:
        curr.append(line.strip())
if curr:
    seqs.append("".join(curr))

for s in seqs:
    gc = gc_fraction(s) * 100
    score = aligner.score(primer, s)
    X.append(gc)
    y.append(score)

X = np.array(X).reshape(-1, 1)
y = np.array(y)

model = LinearRegression()
model.fit(X, y)

print(round(model.coef_[0], 4))
print(round(model.intercept_, 4))
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(script)
        tmp_name = tmp.name

    try:
        result = subprocess.run(
            ["/home/user/venv/bin/python", tmp_name],
            capture_output=True, text=True
        )
        assert result.returncode == 0, "Failed to run verification script in user venv. Are biopython and scikit-learn installed?"

        lines = result.stdout.strip().split("\n")
        assert len(lines) == 2, "Unexpected output from verification script"

        expected_slope = float(lines[0])
        expected_intercept = float(lines[1])

        assert math.isclose(actual_slope, expected_slope, abs_tol=0.0002), f"Slope mismatch. Expected {expected_slope}, got {actual_slope}"
        assert math.isclose(actual_intercept, expected_intercept, abs_tol=0.0002), f"Intercept mismatch. Expected {expected_intercept}, got {actual_intercept}"
    finally:
        os.remove(tmp_name)