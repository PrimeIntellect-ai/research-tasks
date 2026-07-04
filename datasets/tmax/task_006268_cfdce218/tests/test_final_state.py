# test_final_state.py

import os
import json
import statistics
import subprocess

def test_recovered_file_exists():
    path = "/home/user/recovered_transactions.csv"
    assert os.path.isfile(path), f"Recovered file {path} is missing."
    with open(path, 'rb') as f:
        content = f.read()
    assert b"1000000000.1" in content, "Recovered file does not contain expected data."
    assert b"\x00" in content, "Recovered file should contain the original corrupted data with null bytes."

def test_clean_file_correct():
    path = "/home/user/clean_transactions.csv"
    assert os.path.isfile(path), f"Clean file {path} is missing."

    with open(path, 'rb') as f:
        content = f.read()

    assert b"\x00" not in content, "Clean file still contains null bytes."

    lines = content.decode('utf-8').strip().split('\n')
    # 1 header + 5 valid rows = 6 lines
    assert len(lines) == 6, f"Expected 6 lines in clean file, got {len(lines)}."
    assert "amount" in lines[0], "Header is missing or incorrect."

    # Check that we have the correct valid lines
    expected_amounts = ["1000000000.1", "1000000000.2", "1000000000.3", "1000000000.5", "1000000000.7"]
    found_amounts = []
    for line in lines[1:]:
        parts = line.split(',')
        if len(parts) == 2:
            found_amounts.append(parts[1].strip())

    assert found_amounts == expected_amounts, f"Clean file data mismatch. Expected amounts {expected_amounts}, got {found_amounts}."

def test_metrics_syntax_fixed():
    path = "/home/user/fraud_analyzer/metrics.py"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "def calculate_mean(data):" in content or "def calculate_mean" not in content or "def calculate_mean(data)\n" not in content, \
        "Syntax error in metrics.py (missing colon) was not fixed."

    # Verify it compiles
    try:
        compile(content, path, 'exec')
    except SyntaxError as e:
        assert False, f"metrics.py still has a syntax error: {e}"

def test_package_installed():
    try:
        # Check if the package is installed in the current environment
        output = subprocess.check_output(["pip", "show", "fraud-analyzer"]).decode('utf-8')
        assert "Name: fraud-analyzer" in output or "Name: fraud_analyzer" in output, "Package fraud_analyzer is not installed properly."
    except subprocess.CalledProcessError:
        assert False, "Package fraud_analyzer is not installed. Did you run pip install -e /home/user/fraud_analyzer?"

def test_report_json_correct():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"Report file {path} is missing."

    with open(path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, "report.json is not valid JSON."

    assert "count" in report, "Report is missing 'count' key."
    assert "variance" in report, "Report is missing 'variance' key."

    assert report["count"] == 5, f"Expected count to be 5, got {report['count']}."

    amounts = [1000000000.1, 1000000000.2, 1000000000.3, 1000000000.5, 1000000000.7]
    expected_pvariance = statistics.pvariance(amounts)
    expected_variance = statistics.variance(amounts)

    reported_variance = report["variance"]

    # Allow either population variance or sample variance
    is_pvar = abs(reported_variance - expected_pvariance) < 1e-4
    is_var = abs(reported_variance - expected_variance) < 1e-4

    assert is_pvar or is_var, \
        f"Reported variance {reported_variance} does not match expected stable variance (approx {expected_pvariance} or {expected_variance})."