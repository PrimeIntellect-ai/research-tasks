# test_final_state.py

import os
import subprocess
import csv
import stat

def test_c_parser_compiled_and_executable():
    executable = "/home/user/l10n/parse_logs"
    assert os.path.isfile(executable), f"Compiled binary {executable} does not exist."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_c_parser_no_crash():
    executable = "/home/user/l10n/parse_logs"
    input_data = '{"timestamp": 1700014400, "locale": "ja-JP", "message": "Konnichiwa \\u3042"}\n'
    try:
        proc = subprocess.run(
            [executable],
            input=input_data.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"C parser crashed or returned non-zero exit code: {e}")
    except subprocess.TimeoutExpired:
        pytest.fail("C parser timed out.")

    stdout = proc.stdout.decode("utf-8")
    assert "1700014400" in stdout, "Parser output missing timestamp."
    assert "ja-JP" in stdout, "Parser output missing locale."

def test_hourly_counts_csv():
    csv_file = "/home/user/l10n/hourly_counts.csv"
    assert os.path.isfile(csv_file), f"{csv_file} does not exist."

    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{csv_file} is empty."

    parsed_counts = {}
    for row in rows:
        if len(row) != 2:
            continue
        try:
            ts = int(row[0])
            count = int(row[1])
            parsed_counts[ts] = count
        except ValueError:
            continue # Skip header if present

    assert len(parsed_counts) >= 5, "Not enough rows in hourly_counts.csv. Did you fill the gaps?"

    # Check if they used hour indices or hour timestamps (hour * 3600)
    keys = sorted(list(parsed_counts.keys()))
    if keys[0] < 1000000:
        # Likely hour indices
        expected_keys = list(range(472222, 472227))
    else:
        # Likely hour timestamps
        expected_keys = [h * 3600 for h in range(472222, 472227)]

    for k in expected_keys:
        assert k in parsed_counts, f"Missing expected time bin {k} in hourly_counts.csv (gap filling failed)."

    # Check values
    assert parsed_counts[expected_keys[0]] == 1, "Incorrect count for first hour."
    assert parsed_counts[expected_keys[1]] == 1, "Incorrect count for second hour."
    assert parsed_counts[expected_keys[2]] == 0, "Incorrect count for third hour (gap)."
    assert parsed_counts[expected_keys[3]] == 0, "Incorrect count for fourth hour (gap)."
    assert parsed_counts[expected_keys[4]] == 2, "Incorrect count for fifth hour."

def test_stratified_sample():
    tsv_file = "/home/user/l10n/stratified_sample.tsv"
    assert os.path.isfile(tsv_file), f"{tsv_file} does not exist."

    with open(tsv_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    locales_found = set()
    for line in lines:
        parts = line.split("\t")
        if len(parts) >= 2:
            locales_found.add(parts[1])

    assert "en-US" in locales_found, "Missing en-US in stratified sample."
    assert "es-ES" in locales_found, "Missing es-ES in stratified sample."
    assert "ja-JP" in locales_found, "Missing ja-JP in stratified sample."

    # Ensure only the earliest en-US is present
    en_us_lines = [line for line in lines if "\ten-US\t" in line or line.endswith("\ten-US") or len(line.split("\t")) >= 2 and line.split("\t")[1] == "en-US"]
    assert len(en_us_lines) == 1, "There should be exactly one entry per locale in stratified sample."
    assert en_us_lines[0].startswith("1700000000"), "The stratified sample did not pick the earliest entry for en-US."

def test_cron_job():
    try:
        proc = subprocess.run(
            ["crontab", "-l", "-u", "user"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        crontab_out = proc.stdout.decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to list crontab for 'user'.")

    lines = [line.strip() for line in crontab_out.splitlines() if line.strip() and not line.startswith("#")]

    cron_found = False
    for line in lines:
        parts = line.split()
        if len(parts) >= 6:
            minute = parts[0]
            cmd = " ".join(parts[5:])
            if minute == "0" and "/home/user/l10n/process.sh" in cmd:
                cron_found = True
                break

    assert cron_found, "Cron job for user not found or incorrectly scheduled. Expected minute '0' and command '/home/user/l10n/process.sh'."