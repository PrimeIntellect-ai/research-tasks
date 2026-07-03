# test_final_state.py
import os
import csv
import datetime
import calendar

def parse_legacy_time(ts_str):
    # Format: YYYY/MM/DD HH:MM:SS (Assumed UTC)
    dt = datetime.datetime.strptime(ts_str, "%Y/%m/%d %H:%M:%S")
    return calendar.timegm(dt.utctimetuple())

def parse_app_time(ts_str):
    # Format: YYYY-MM-DDTHH:MM:SSZ (ISO 8601, UTC)
    dt = datetime.datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
    return calendar.timegm(dt.utctimetuple())

def process_row(row, time_parser):
    ts_str, name, email, ip, age_str, score_str = row

    try:
        age = int(age_str)
        score = int(score_str)
    except ValueError:
        return None

    if not (18 <= age <= 100):
        return None
    if not (0 <= score <= 1000):
        return None

    epoch = time_parser(ts_str)

    email_parts = email.split('@')
    if len(email_parts) == 2:
        masked_email = f"***@{email_parts[1]}"
    else:
        masked_email = email # fallback if malformed

    ip_parts = ip.split('.')
    if len(ip_parts) == 4:
        masked_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0"
    else:
        masked_ip = ip # fallback if malformed

    return (epoch, masked_email, masked_ip, age, score)

def compute_expected_output():
    results = []

    legacy_path = "/home/user/data/legacy.csv"
    if os.path.exists(legacy_path):
        with open(legacy_path, "r", encoding="iso-8859-1") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 6:
                    processed = process_row(row, parse_legacy_time)
                    if processed:
                        results.append(processed)

    app_path = "/home/user/data/app.csv"
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 6:
                    processed = process_row(row, parse_app_time)
                    if processed:
                        results.append(processed)

    results.sort(key=lambda x: x[0])

    output_lines = []
    for r in results:
        output_lines.append(f"{r[0]},{r[1]},{r[2]},{r[3]},{r[4]}")

    return "\n".join(output_lines) + "\n"

def test_script_exists():
    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_cleaned_logs_exists():
    output_path = "/home/user/cleaned_logs.csv"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

def test_cleaned_logs_content():
    output_path = "/home/user/cleaned_logs.csv"
    assert os.path.isfile(output_path), "Cannot check content because output file is missing."

    with open(output_path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    # Standardize line endings for comparison
    actual_lines = [line.strip() for line in actual_content.strip().splitlines()]

    expected_content = compute_expected_output()
    expected_lines = [line.strip() for line in expected_content.strip().splitlines()]

    assert actual_lines == expected_lines, (
        "The content of /home/user/cleaned_logs.csv does not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )