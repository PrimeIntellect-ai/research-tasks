# test_final_state.py
import os
import json

def test_script_exists():
    script_path = "/home/user/process_storage.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_cleaned_gcode_files():
    expected_print1 = [
        "G21",
        "G90",
        "G1 X100 Y100 F1500",
        "M104 S200"
    ]
    expected_print2 = [
        "M109 S200",
        "G1 Z0.2 F1200",
        "G1 X110 Y110 E1.5"
    ]

    print1_path = "/home/user/cleaned_gcode/print1.gcode"
    print2_path = "/home/user/cleaned_gcode/print2.gcode"

    assert os.path.isfile(print1_path), f"Cleaned GCode file missing: {print1_path}"
    assert os.path.isfile(print2_path), f"Cleaned GCode file missing: {print2_path}"

    with open(print1_path, 'r') as f:
        content1 = f.read().splitlines()
    assert content1 == expected_print1, f"Content of {print1_path} is incorrect. Expected {expected_print1}, got {content1}"

    with open(print2_path, 'r') as f:
        content2 = f.read().splitlines()
    assert content2 == expected_print2, f"Content of {print2_path} is incorrect. Expected {expected_print2}, got {content2}"

def test_storage_report():
    report_path = "/home/user/storage_report.json"
    assert os.path.isfile(report_path), f"Report file missing: {report_path}"

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not a valid JSON file."

    assert "processed_gcode_count" in report, "Missing 'processed_gcode_count' in report."
    assert report["processed_gcode_count"] == 2, f"Incorrect 'processed_gcode_count' in report. Expected 2, got {report['processed_gcode_count']}"

    assert "corrupt_archives" in report, "Missing 'corrupt_archives' in report."
    expected_corrupt = ["/home/user/storage_pool/proj2/broken_backup.tar.gz"]
    assert report["corrupt_archives"] == expected_corrupt, f"Incorrect 'corrupt_archives' in report. Expected {expected_corrupt}, got {report['corrupt_archives']}"