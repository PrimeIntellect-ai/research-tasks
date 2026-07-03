# test_final_state.py
import os
import subprocess
import requests
import pytest

def test_translations_wide_csv():
    csv_path = "/home/user/translations_wide.csv"
    assert os.path.exists(csv_path), f"{csv_path} does not exist"

    with open(csv_path, 'r') as f:
        content = f.read().strip().split('\n')

    expected_header = "key,en,es,fr"
    assert expected_header in content[0], "Header of CSV is incorrect"

    # Check rows (order of rows might vary, but spec says 'logout' then 'welcome' or similar)
    expected_rows = [
        "logout,Sign out,,",
        "welcome,Welcome,bienvenido,Bienvenue!"
    ]

    for row in expected_rows:
        assert any(row in line for line in content), f"Expected row '{row}' not found in {csv_path}"

def test_http_server():
    try:
        response = requests.get("http://127.0.0.1:8080/translations", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP server is not reachable on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "text/csv" in response.headers.get("Content-Type", ""), "Expected Content-Type: text/csv"

    content = response.text.strip().split('\n')
    assert "key,en,es,fr" in content[0], "Response CSV header is incorrect"

    expected_rows = [
        "logout,Sign out,,",
        "welcome,Welcome,bienvenido,Bienvenue!"
    ]
    for row in expected_rows:
        assert any(row in line for line in content), f"Expected row '{row}' not found in server response"

def test_cron_job():
    try:
        crontab_output = subprocess.check_output(["crontab", "-l"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("No crontab found for the current user")

    # Check for the expected cron job
    expected_command_part = "cp /home/user/translations_wide.csv /home/user/backups/translations_wide_$(date +\\%Y\\%m\\%d\\%H\\%M).csv"
    assert expected_command_part in crontab_output or expected_command_part.replace("\\%", "%") in crontab_output, "Cron job command is missing or incorrect"
    assert "0 * * * *" in crontab_output, "Cron schedule is missing or incorrect"