# test_final_state.py
import os
import stat
import subprocess
import csv

def test_script_exists_and_executable():
    script_path = "/home/user/process_loc.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_run_script():
    # Execute the script to ensure it produces the expected output
    result = subprocess.run(["/home/user/process_loc.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error:\n{result.stderr}"

def test_cleaned_csv():
    cleaned_path = "/home/user/output/cleaned.csv"
    assert os.path.isfile(cleaned_path), f"File {cleaned_path} does not exist."

    expected_rows = [
        ["T001", "es", "1696204800", "carlos@anonymized.local", "150"],
        ["T002", "fr", "1696204900", "marie@anonymized.local", "200"],
        ["T004", "es", "1696291200", "luis@anonymized.local", "300"],
        ["T005", "fr", "1696291200", "luc@anonymized.local", "110"],
        ["T003", "de", "1696291500", "hans@anonymized.local", "95"]
    ]

    with open(cleaned_path, "r") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    # Sort expected and actual rows by timestamp to ensure proper comparison
    expected_sorted = sorted(expected_rows, key=lambda x: int(x[2]))
    actual_sorted = sorted(actual_rows, key=lambda x: int(x[2]))

    assert actual_rows == actual_sorted, "cleaned.csv is not sorted by timestamp in ascending order."

    # Check if rows match exactly
    # Since there are rows with the same timestamp, their relative order might differ, 
    # but the problem implies sorting by timestamp. Let's check sets and then sort order.
    assert len(actual_rows) == len(expected_rows), "cleaned.csv does not have the correct number of rows."

    for row in expected_rows:
        assert row in actual_rows, f"Expected row {row} not found in cleaned.csv."

def test_cumulative_stats_csv():
    stats_path = "/home/user/output/cumulative_stats.csv"
    assert os.path.isfile(stats_path), f"File {stats_path} does not exist."

    expected_rows = [
        ["1696204800", "es", "150"],
        ["1696204900", "fr", "200"],
        ["1696291200", "es", "450"],
        ["1696291200", "fr", "310"],
        ["1696291500", "de", "95"]
    ]

    with open(stats_path, "r") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    actual_sorted = sorted(actual_rows, key=lambda x: int(x[0]))
    assert actual_rows == actual_sorted, "cumulative_stats.csv is not sorted by timestamp in ascending order."

    assert len(actual_rows) == len(expected_rows), "cumulative_stats.csv does not have the correct number of rows."

    for row in expected_rows:
        assert row in actual_rows, f"Expected row {row} not found in cumulative_stats.csv."

def test_cron_job():
    # Check if crontab contains the expected job
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."

    cron_lines = [line.strip() for line in result.stdout.split('\n') if line.strip() and not line.startswith('#')]

    expected_command = "/home/user/process_loc.sh"
    found = False
    for line in cron_lines:
        parts = line.split()
        if len(parts) >= 6:
            minute, hour, dom, mon, dow = parts[:5]
            command = " ".join(parts[5:])
            if minute == "15" and hour == "3" and dom == "*" and mon == "*" and dow == "*" and expected_command in command:
                found = True
                break

    assert found, "Cron job for /home/user/process_loc.sh at 03:15 AM is not set correctly."