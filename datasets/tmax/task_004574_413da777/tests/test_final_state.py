# test_final_state.py

import os
import stat

def test_report_file_exists():
    path = "/home/user/report.txt"
    assert os.path.exists(path), f"File {path} does not exist. Did you create the report?"
    assert os.path.isfile(path), f"{path} is not a regular file."

def test_report_file_permissions():
    path = "/home/user/report.txt"
    st = os.stat(path)
    # Check if owner has read and write permissions
    assert bool(st.st_mode & stat.S_IRUSR), f"Owner does not have read permission on {path}."
    assert bool(st.st_mode & stat.S_IWUSR), f"Owner does not have write permission on {path}."

def test_report_file_contents():
    path = "/home/user/report.txt"
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_session = "SESSION_ID=abc123xyz890"
    expected_redirect = "REDIRECT_URL=http://malicious-site.local/redirect_target"

    assert len(lines) == 2, f"Expected exactly 2 non-empty lines in {path}, found {len(lines)}."
    assert expected_session in lines, f"Could not find the correct SESSION_ID line in {path}."
    assert expected_redirect in lines, f"Could not find the correct REDIRECT_URL line in {path}."

    # Check exact order if required, but containment is usually sufficient for this type of task
    assert lines[0] == expected_session, f"First line should be {expected_session}, got {lines[0]}."
    assert lines[1] == expected_redirect, f"Second line should be {expected_redirect}, got {lines[1]}."