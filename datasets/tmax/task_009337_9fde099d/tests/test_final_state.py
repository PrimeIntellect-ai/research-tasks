# test_final_state.py

import os
import csv
import pytest

REPORT_FILE = '/home/user/matrix_prep/report.csv'

def test_report_file_exists():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."

def test_report_content():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."

    with open(REPORT_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 11, f"Expected 11 rows (1 header + 10 data), found {len(rows)}"
    assert rows[0] == ['matrix_id', 'status', 'error'], f"Invalid header: {rows[0]}"

    expected_stable = {0, 3, 6, 9}
    expected_failed = {2, 5, 8}

    found_ids = set()

    for row in rows[1:]:
        assert len(row) == 3, f"Row does not have 3 columns: {row}"
        try:
            mid = int(row[0])
        except ValueError:
            pytest.fail(f"matrix_id must be an integer, got: {row[0]}")

        status = row[1]
        assert status in {'stable', 'unstable', 'failed'}, f"Invalid status: {status}"

        try:
            err = float(row[2])
        except ValueError:
            pytest.fail(f"error must be a float, got: {row[2]}")

        # Check scientific notation format (e.g., -1.000000e+00)
        # We can just verify it parses as float and has 'e' or 'E' in the string
        assert 'e' in row[2].lower(), f"error must be in scientific notation, got: {row[2]}"

        found_ids.add(mid)

        if mid in expected_stable:
            assert status == 'stable', f"Matrix {mid} should be stable, got {status}"
            assert 0 <= err <= 1e-8, f"Matrix {mid} has invalid error for stable status: {err}"

        if mid in expected_failed:
            assert status == 'failed', f"Matrix {mid} should be failed, got {status}"
            assert err == -1.0, f"Matrix {mid} error should be -1.0, got {err}"

        if status == 'failed':
            assert err == -1.0, f"Failed matrix {mid} error should be -1.0, got {err}"
        elif status == 'stable':
            assert 0 <= err <= 1e-8, f"Stable matrix {mid} has invalid error: {err}"
        elif status == 'unstable':
            assert err > 1e-8, f"Unstable matrix {mid} has invalid error: {err}"

    assert found_ids == set(range(10)), f"Missing or extra matrix IDs. Found: {found_ids}"