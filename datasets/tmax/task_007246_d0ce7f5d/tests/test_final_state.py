# test_final_state.py
import os

def test_archive_report_csv_contents():
    report_path = "/home/user/archive_report.csv"
    assert os.path.isfile(report_path), f"The report file {report_path} was not created."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "filename,total_size\n"
        "node2.json.gz,2048\n"
        "node3.json.gz,4096\n"
        "node5.json.gz,8192"
    )

    # Compare line by line to ignore trailing newlines and provide better diffs
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = expected_content.splitlines()

    assert actual_lines == expected_lines, "The contents of archive_report.csv do not match the expected output."

def test_log_dumps_directory_contents():
    log_dir = "/home/user/log_dumps"
    assert os.path.isdir(log_dir), f"The directory {log_dir} is missing."

    expected_files = {
        "node1.json.gz",
        "node2.json.gz.processed",
        "node3.json.gz.processed",
        "node4.json.gz",
        "node5.json.gz.processed"
    }

    actual_files = set(os.listdir(log_dir))

    # Check that all expected files exist
    for f in expected_files:
        assert f in actual_files, f"Expected file {f} is missing from {log_dir}."

    # Check that the original files for the processed ones are gone
    unexpected_files = {
        "node2.json.gz",
        "node3.json.gz",
        "node5.json.gz",
        "node1.json.gz.processed",
        "node4.json.gz.processed"
    }

    for f in unexpected_files:
        assert f not in actual_files, f"File {f} should not exist in {log_dir}."