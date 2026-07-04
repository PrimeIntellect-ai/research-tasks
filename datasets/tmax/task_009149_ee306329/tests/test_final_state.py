# test_final_state.py

import os

def test_pipeline_log_exists_and_content():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[INFO] Successfully processed SRV-01 with 6 records.",
        "[INFO] Successfully processed SRV-02 with 4 records.",
        "[INFO] Successfully processed SRV-03 with 3 records."
    ]

    # Check that the expected lines are present and in alphabetical order
    for expected in expected_lines:
        assert expected in lines, f"Expected log line '{expected}' not found in {log_path}."

    # Verify order
    indices = [lines.index(expected) for expected in expected_lines]
    assert indices == sorted(indices), "Log lines are not in alphabetical order of server_id."

def test_srv01_report():
    report_path = "/home/user/reports/SRV-01_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read()

    assert "Server: SRV-01" in content, "Missing or incorrect Server line in SRV-01 report."
    assert "Total Records: 6" in content, "Missing or incorrect Total Records line in SRV-01 report."
    assert "Max Temp: 50.00" in content, "Missing or incorrect Max Temp line in SRV-01 report."
    assert "Average Temp: 45.00" in content, "Missing or incorrect Average Temp line in SRV-01 report."

def test_srv02_report():
    report_path = "/home/user/reports/SRV-02_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read()

    assert "Server: SRV-02" in content, "Missing or incorrect Server line in SRV-02 report."
    assert "Total Records: 4" in content, "Missing or incorrect Total Records line in SRV-02 report."
    assert "Max Temp: 66.00" in content, "Missing or incorrect Max Temp line in SRV-02 report."
    assert "Average Temp: 63.00" in content, "Missing or incorrect Average Temp line in SRV-02 report."

def test_srv03_report():
    report_path = "/home/user/reports/SRV-03_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read()

    assert "Server: SRV-03" in content, "Missing or incorrect Server line in SRV-03 report."
    assert "Total Records: 3" in content, "Missing or incorrect Total Records line in SRV-03 report."
    assert "Max Temp: 40.00" in content, "Missing or incorrect Max Temp line in SRV-03 report."
    assert "Average Temp: 35.00" in content, "Missing or incorrect Average Temp line in SRV-03 report."