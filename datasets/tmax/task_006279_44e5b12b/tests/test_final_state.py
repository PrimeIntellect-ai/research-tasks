# test_final_state.py
import os
import subprocess

def test_executable_exists():
    executable = "/home/user/bin/log_parser"
    assert os.path.isfile(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_clean_messages_output():
    output_file = "/home/user/logs/clean_messages.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "user admin logged in!",
        "database connection reset",
        "cache miss for key 123"
    }

    actual_lines = set(lines)

    assert actual_lines == expected_lines, f"Expected {expected_lines}, but got {actual_lines}"
    assert len(lines) == len(expected_lines), "Output contains duplicate lines or incorrect number of lines."

def test_cron_job_scheduled():
    try:
        # Run crontab -l for the current user (assuming the tests run as the same user or root)
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        crontab_content = ""

    # Check if there's a cron job scheduled at 02:00
    cron_lines = [line.strip() for line in crontab_content.splitlines() if line.strip() and not line.strip().startswith('#')]

    found_cron = False
    for line in cron_lines:
        parts = line.split()
        if len(parts) >= 5:
            minute, hour, dom, mon, dow = parts[:5]
            if minute == "0" and hour == "2" and dom == "*" and mon == "*" and dow == "*":
                # Check if it mentions the required files
                if "raw_logs.jsonl" in line and "clean_messages.txt" in line:
                    found_cron = True
                    break
                elif "log_parser" in line or ".sh" in line:
                    # It might be calling a script or just the binary with redirection
                    found_cron = True
                    break

    assert found_cron, "Could not find a valid cron job scheduled at 02:00 AM ('0 2 * * *') for the pipeline."