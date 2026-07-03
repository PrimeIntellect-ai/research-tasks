# test_final_state.py

import os
import json
import csv
from datetime import datetime, timedelta

def parse_iso_time(t_str):
    return datetime.strptime(t_str, "%Y-%m-%dT%H:%M:%SZ")

def parse_db_time(t_str):
    return datetime.strptime(t_str, "%d/%b/%Y:%H:%M:%S +0000")

def test_report_exists():
    assert os.path.exists("/home/user/report.md"), "The report.md file was not generated."
    assert not os.path.exists("/home/user/error.log"), "An error.log was generated, but the logs were in chronological order."

def test_report_content():
    # Recompute the expected report based on the files
    auth_file = "/home/user/logs/auth.jsonl"
    api_file = "/home/user/logs/api.csv"
    db_file = "/home/user/logs/db.log"

    assert os.path.exists(auth_file)
    assert os.path.exists(api_file)
    assert os.path.exists(db_file)

    failed_logins = []
    with open(auth_file, "r") as f:
        for line in f:
            if not line.strip(): continue
            data = json.loads(line)
            if data.get("event") == "login_failed":
                failed_logins.append(data)

    api_requests = []
    with open(api_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            api_requests.append(row)

    db_logs = []
    with open(db_file, "r") as f:
        for line in f:
            if not line.strip(): continue
            # Format: [DD/MMM/YYYY:HH:MM:SS +0000] <LEVEL>: <Message>
            time_part, rest = line.split("]", 1)
            time_str = time_part[1:]
            msg_part = rest.strip()
            db_logs.append({"time": time_str, "msg": msg_part})

    expected_lines = ["# Incident Report"]

    for login in failed_logins:
        auth_time = parse_iso_time(login["timestamp"])
        user = login["user"]
        ip = login["ip"]

        expected_lines.append("")
        expected_lines.append(f"## Failed Login for user: {user} at {login['timestamp']}")
        expected_lines.append(f"- IP Address: {ip}")

        # Match API requests
        matched_api = 0
        for req in api_requests:
            if req["ip"] == ip:
                req_time = parse_iso_time(req["timestamp"])
                if abs((req_time - auth_time).total_seconds()) <= 5:
                    matched_api += 1

        expected_lines.append(f"- Matched API Requests: {matched_api}")
        expected_lines.append("- DB Logs:")

        # Match DB logs
        matched_db = []
        for dbl in db_logs:
            db_time = parse_db_time(dbl["time"])
            if f"user {user}" in dbl["msg"]:
                if abs((db_time - auth_time).total_seconds()) <= 5:
                    matched_db.append(dbl["msg"])

        if not matched_db:
            expected_lines.append("  - None")
        else:
            for m in matched_db:
                expected_lines.append(f"  - {m}")

    expected_report = "\n".join(expected_lines) + "\n"

    with open("/home/user/report.md", "r") as f:
        actual_report = f.read()

    # We do a line-by-line comparison to be robust against trailing newlines
    actual_lines = [line.strip() for line in actual_report.strip().split("\n")]
    expected_lines_clean = [line.strip() for line in expected_report.strip().split("\n")]

    assert actual_lines == expected_lines_clean, "The generated report.md does not match the expected recomputed output."