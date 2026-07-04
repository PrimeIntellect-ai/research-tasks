# test_final_state.py

import os
import subprocess
import pytest

PROCESS_GO_PATH = "/home/user/process.go"
SETUP_CRON_PATH = "/home/user/setup_cron.sh"
PROCESSED_DATA_PATH = "/home/user/processed_data.csv"

EXPECTED_PROCESSED_DATA = """id,masked_email,distance
4,***@site.net,0.00
3,***@domain.com,30.50
9,***@tech.co,30.50
6,***@hello.com,90.00
1,***@example.com,114.71"""

def test_go_program_exists():
    """Ensure process.go was created."""
    assert os.path.isfile(PROCESS_GO_PATH), f"Go program {PROCESS_GO_PATH} does not exist."

def test_setup_cron_script_exists():
    """Ensure setup_cron.sh was created."""
    assert os.path.isfile(SETUP_CRON_PATH), f"Bash script {SETUP_CRON_PATH} does not exist."

def test_processed_data_correct():
    """Verify the contents of processed_data.csv."""
    assert os.path.isfile(PROCESSED_DATA_PATH), f"Processed data file {PROCESSED_DATA_PATH} does not exist."

    with open(PROCESSED_DATA_PATH, "r") as f:
        content = f.read().strip()

    assert content == EXPECTED_PROCESSED_DATA, (
        f"Contents of {PROCESSED_DATA_PATH} do not match the expected output.\n"
        f"Expected:\n{EXPECTED_PROCESSED_DATA}\n\nGot:\n{content}"
    )

def test_crontab_installed():
    """Check if the correct cron job is installed for the current user."""
    try:
        # We run crontab -l. The task says "for the current user", which is usually the user running the tests.
        # Since tests run as the user, we just use `crontab -l`.
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it installed?")

    expected_cron_job = "0 2 * * * cd /home/user && go run /home/user/process.go"

    # Check if the expected string is in the crontab output
    # Allow for multiple spaces or slightly different formatting by checking the exact string line by line
    found = any(expected_cron_job in line for line in crontab_output.splitlines())

    assert found, f"Expected cron job '{expected_cron_job}' not found in crontab.\nCurrent crontab:\n{crontab_output}"