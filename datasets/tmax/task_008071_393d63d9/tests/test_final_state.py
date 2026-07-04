# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/process_loc.py"
CRON_PATH = "/home/user/cron_schedule.txt"
MASTER_PATH = "/home/user/master_en.json"
INCOMING_PATH = "/home/user/incoming_fr.json"
REPORT_PATH = "/home/user/loc_report.json"
APPROVED_PATH = "/home/user/approved_fr.json"

def test_cron_schedule():
    """Test that the cron schedule file exists and contains the correct crontab entry."""
    assert os.path.isfile(CRON_PATH), f"Missing file: {CRON_PATH}"

    with open(CRON_PATH, "r") as f:
        content = f.read().strip()

    expected_cron = "0 2 * * * python3 /home/user/process_loc.py"
    assert expected_cron in content, f"Crontab entry is incorrect. Expected '{expected_cron}', but got '{content}'"

def test_script_exists_and_runs():
    """Test that the python script exists and runs without errors."""
    assert os.path.isfile(SCRIPT_PATH), f"Missing script: {SCRIPT_PATH}"

    # Run the script to generate/update the outputs
    result = subprocess.run(["python3", SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to run: {result.stderr}"

def test_loc_report():
    """Test that loc_report.json is generated correctly."""
    assert os.path.isfile(REPORT_PATH), f"Missing file: {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not valid JSON")

    assert "anomalies" in report, "Missing 'anomalies' key in loc_report.json"
    assert "missing" in report, "Missing 'missing' key in loc_report.json"

    assert report["anomalies"] == ["login_button"], "Anomalies list is incorrect"
    assert report["missing"] == ["footer_text", "promo_code"], "Missing list is incorrect"

def test_approved_fr():
    """Test that approved_fr.json is generated correctly."""
    assert os.path.isfile(APPROVED_PATH), f"Missing file: {APPROVED_PATH}"

    with open(APPROVED_PATH, "r") as f:
        try:
            approved = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{APPROVED_PATH} is not valid JSON")

    expected_approved = {
        "checkout_cart": "Caisse",
        "error_404": "Page non trouvee.",
        "welcome_message": "Bienvenue!"
    }

    assert approved == expected_approved, f"Approved translations are incorrect. Expected {expected_approved}, got {approved}"