# test_final_state.py
import os
import subprocess
import pytest

def test_parser_script_exists_and_executable():
    script_path = "/home/user/parser.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_extracted_errors_log():
    log_path = "/home/user/extracted_errors.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run your script?"

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "1697114100|Connexion échouée à la base de données",
        "1697114700|致命的なエラーが発生しました",
        "1697116222|Fichier introuvable",
        "1697116530|タイムアウト例外"
    ]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual}'"

def test_cron_job_installed():
    try:
        result = subprocess.run(
            ["crontab", "-l", "-u", "user"],
            capture_output=True,
            text=True,
            check=True
        )
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to retrieve crontab for user 'user'.")

    cron_lines = [line.strip() for line in crontab_output.splitlines() if line.strip() and not line.strip().startswith("#")]

    found = False
    for line in cron_lines:
        parts = line.split()
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            command = " ".join(parts[5:])
            if schedule == "*/5 * * * *" and "parser.sh" in command:
                found = True
                break

    assert found, "Could not find a cron job for 'user' running parser.sh every 5 minutes (*/5 * * * *)."