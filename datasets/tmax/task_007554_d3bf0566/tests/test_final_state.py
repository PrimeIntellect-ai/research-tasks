# test_final_state.py
import os

def test_hidden_archives_report():
    report_path = '/home/user/hidden_archives.log'
    assert os.path.exists(report_path), f"Report file {report_path} was not created."

    expected_files = [
        ('/home/user/user_uploads/financials.csv', 'GZIP'),
        ('/home/user/user_uploads/notes.txt', 'GZIP'),
        ('/home/user/user_uploads/system_cache.dat', 'ZIP')
    ]

    expected_lines = []
    for filepath, archive_type in expected_files:
        assert os.path.exists(filepath), f"Expected file {filepath} is missing from the system."
        size = os.path.getsize(filepath)
        expected_lines.append(f"{filepath}|{archive_type}|{size}")

    # Sort alphabetically by full file path (which is already done in expected_files)
    expected_lines.sort()

    with open(report_path, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Report contents do not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )