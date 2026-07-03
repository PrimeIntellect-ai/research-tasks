# test_final_state.py

import os
import subprocess

def test_output_file_content():
    output_file = "/home/user/hourly_unique_translations.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"{output_file} is not a regular file."

    expected_content = (
        "2023-10-24T14|es|¡Hola!\n"
        "2023-10-24T14|fr|Bonjour\n"
        "2023-10-24T14|ja|こんにちは\n"
        "2023-10-24T15|es|Adiós\n"
        "2023-10-24T15|ja|さようなら\n"
    )

    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Strip trailing newlines for comparison to be robust
    assert content.strip() == expected_content.strip(), "The contents of the output file do not match the expected deduplicated and sorted output."

def test_executable_exists_and_is_executable():
    executable_path = "/home/user/dedup"
    assert os.path.exists(executable_path), f"Compiled executable {executable_path} does not exist."
    assert os.path.isfile(executable_path), f"{executable_path} is not a file."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_crontab_scheduled():
    try:
        result = subprocess.run(
            ["crontab", "-u", "user", "-l"],
            capture_output=True,
            text=True,
            check=True
        )
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        assert False, "Failed to read crontab for 'user'. Ensure the crontab exists."

    expected_cron_job = "0 * * * * /home/user/dedup"

    # Check if the expected cron job is present in the crontab (ignoring leading/trailing whitespace)
    found = any(expected_cron_job in line for line in crontab_content.splitlines())
    assert found, f"Crontab for 'user' does not contain the expected job: {expected_cron_job}"