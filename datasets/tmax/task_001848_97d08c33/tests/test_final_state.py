# test_final_state.py
import os
import time
import subprocess
import csv
from collections import defaultdict

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.exists(log_path), f"Log file not found at {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[INFO] ETL extraction completed successfully.",
        "[INFO] HTML report generated."
    ]

    assert lines == expected_lines, f"Expected pipeline.log to contain exactly {expected_lines}, but got {lines}"

def test_execution_time():
    binary_path = "/app/fastlog_etl-1.0.0/bin/fastlog_etl"
    input_path = "/home/user/api_logs.csv"

    assert os.path.exists(binary_path), f"Binary not found at {binary_path}"
    assert os.path.exists(input_path), f"Input file not found at {input_path}"

    # Measure execution time
    start_time = time.time()
    with open(input_path, "r") as f:
        result = subprocess.run([binary_path], stdin=f, capture_output=True, text=True)
    end_time = time.time()

    assert result.returncode == 0, f"Binary execution failed with stderr: {result.stderr}"

    execution_time = end_time - start_time
    threshold = 1.5

    assert execution_time <= threshold, (
        f"Execution time {execution_time:.3f}s exceeds threshold of {threshold}s. "
        "Ensure qsort is used and -O3 optimization is enabled."
    )

def test_summary_csv_and_html_report():
    input_path = "/home/user/api_logs.csv"
    summary_path = "/home/user/summary.csv"
    report_path = "/home/user/report.html"

    assert os.path.exists(summary_path), f"Summary CSV not found at {summary_path}"
    assert os.path.exists(report_path), f"HTML report not found at {report_path}"

    # Recompute expected summary
    endpoints_data = defaultdict(lambda: {"count": 0, "total_latency": 0})
    with open(input_path, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 3:
                ep = parts[1]
                lat = int(parts[2])
                endpoints_data[ep]["count"] += 1
                endpoints_data[ep]["total_latency"] += lat

    expected_summary = []
    for ep in sorted(endpoints_data.keys()):
        count = endpoints_data[ep]["count"]
        avg_lat = endpoints_data[ep]["total_latency"] // count
        expected_summary.append((ep, count, avg_lat))

    # Check summary.csv
    actual_summary = []
    with open(summary_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                actual_summary.append((row[0], int(row[1]), int(row[2])))

    assert actual_summary == expected_summary, f"Summary CSV contents {actual_summary} do not match expected {expected_summary}"

    # Check HTML report
    with open(report_path, "r") as f:
        html_content = f.read()

    assert "<html>" in html_content and "</html>" in html_content, "HTML report missing <html> tags"
    assert "<body>" in html_content and "</body>" in html_content, "HTML report missing <body> tags"
    assert "<h1>ETL Pipeline Report</h1>" in html_content, "HTML report missing expected <h1> header"
    assert "<ul>" in html_content and "</ul>" in html_content, "HTML report missing <ul> tags"

    for ep, count, avg_lat in expected_summary:
        expected_li = f"<li>Endpoint: {ep} | Count: {count} | Avg Latency: {avg_lat}ms</li>"
        assert expected_li in html_content, f"HTML report missing expected list item: {expected_li}"