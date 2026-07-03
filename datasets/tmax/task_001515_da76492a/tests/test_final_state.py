# test_final_state.py
import csv
import os
import re
from datetime import datetime, timedelta

PROCESSED_CSV = '/home/user/processed_logs.csv'
REPORT_MD = '/home/user/report.md'
RAW_CSV = '/home/user/raw_logs.csv'

def test_files_exist():
    assert os.path.exists(PROCESSED_CSV), f"Processed CSV not found at {PROCESSED_CSV}"
    assert os.path.exists(REPORT_MD), f"Report markdown not found at {REPORT_MD}"

def test_processed_csv_structure_and_sorting():
    with open(PROCESSED_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['timestamp', 'service', 'message', 'error_count_3h'], \
            f"Unexpected header in processed CSV: {header}"

        rows = list(reader)
        assert len(rows) == 15, f"Expected 15 rows in processed CSV, found {len(rows)}"

        # Check sorting: service ascending, timestamp ascending
        services = [row[1] for row in rows]
        timestamps = [row[0] for row in rows]

        expected_services = sorted(services)
        assert services == expected_services, "CSV is not sorted by service ascending."

        # Check timestamps within each service
        for svc in ['APP', 'DB', 'WEB']:
            svc_times = [row[0] for row in rows if row[1] == svc]
            expected_times = sorted(svc_times)
            assert svc_times == expected_times, f"CSV is not sorted by timestamp ascending for service {svc}."

def test_processed_csv_content():
    with open(PROCESSED_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Helper to find a specific row
    def get_row(service, timestamp):
        for row in data:
            if row['service'] == service and row['timestamp'] == timestamp:
                return row
        return None

    # Check APP at 10:00:00 (concatenated)
    app_10 = get_row('APP', '2023-10-01 10:00:00')
    assert app_10 is not None
    assert app_10['message'] == 'Started process [INFO] All good | [ERROR] Failed to fetch'
    assert float(app_10['error_count_3h']) == 1.0

    # Check APP at 12:00:00
    app_12 = get_row('APP', '2023-10-01 12:00:00')
    assert app_12 is not None
    assert app_12['message'] == '[ERROR] Crash Dump saved'
    assert float(app_12['error_count_3h']) == 2.0

    # Check DB at 10:00:00 (newline replaced)
    db_10 = get_row('DB', '2023-10-01 10:00:00')
    assert db_10 is not None
    assert db_10['message'] == '[ERROR] Timeout Retrying'
    assert float(db_10['error_count_3h']) == 1.0

    # Check WEB at 12:00:00
    web_12 = get_row('WEB', '2023-10-01 12:00:00')
    assert web_12 is not None
    assert web_12['message'] == '[ERROR] 500 Internal'
    assert float(web_12['error_count_3h']) == 1.0

    # Check NO_DATA filling
    app_11 = get_row('APP', '2023-10-01 11:00:00')
    assert app_11 is not None
    assert app_11['message'] == 'NO_DATA'
    assert float(app_11['error_count_3h']) == 1.0

    app_13 = get_row('APP', '2023-10-01 13:00:00')
    assert app_13 is not None
    assert app_13['message'] == 'NO_DATA'
    assert float(app_13['error_count_3h']) == 1.0

    app_14 = get_row('APP', '2023-10-01 14:00:00')
    assert app_14 is not None
    assert app_14['message'] == 'NO_DATA'
    assert float(app_14['error_count_3h']) == 0.0

def test_report_content():
    with open(REPORT_MD, 'r', encoding='utf-8') as f:
        report = f.read()

    # Check structure and values
    assert "# Service Report" in report, "Report missing main title."

    # APP section
    assert "## APP" in report, "Report missing APP section."
    assert re.search(r"Max 3H Errors:\s*2(?:\.0)?", report), "APP Max 3H Errors should be 2"

    # DB section
    assert "## DB" in report, "Report missing DB section."
    assert re.search(r"Max 3H Errors:\s*1(?:\.0)?", report), "DB Max 3H Errors should be 1"

    # WEB section
    assert "## WEB" in report, "Report missing WEB section."
    assert re.search(r"Max 3H Errors:\s*1(?:\.0)?", report), "WEB Max 3H Errors should be 1"

    # Check Latest Message for all (all should end with NO_DATA at 14:00:00)
    assert report.count("Latest Message: NO_DATA") == 3, "All services should have 'NO_DATA' as the latest message."