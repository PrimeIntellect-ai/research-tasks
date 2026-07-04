# test_final_state.py
import os
import json
import subprocess
import pytest

def test_files_exist():
    """Verify that the required files have been created."""
    required_files = [
        "/home/user/parser.cpp",
        "/home/user/parser",
        "/home/user/setup_cron.sh",
        "/home/user/processed_locales.jsonl"
    ]
    for file_path in required_files:
        assert os.path.exists(file_path), f"Required file {file_path} is missing."
        assert os.path.isfile(file_path), f"{file_path} is not a regular file."

def test_executable():
    """Verify that the compiled parser is executable."""
    assert os.access("/home/user/parser", os.X_OK), "/home/user/parser is not executable."

def test_jsonl_output():
    """Verify the content of the processed JSONL file."""
    output_path = "/home/user/processed_locales.jsonl"

    expected_data = [
        {"id": "1", "timestamp": "2023-10-05T14:30:00Z", "lang": "es", "text": "Hola,\nmundo"},
        {"id": "2", "timestamp": "2023-10-06T09:15:00Z", "lang": "fr", "text": "Bonjour le monde"},
        {"id": "3", "timestamp": "2023-10-07T11:00:22Z", "lang": "de", "text": "Das ist ein \"Test\"\nmit\nneuen Zeilen"}
    ]

    with open(output_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_data), f"Expected {len(expected_data)} lines in JSONL, found {len(lines)}."

    for i, (line, expected) in enumerate(zip(lines, expected_data)):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

        assert parsed == expected, f"Line {i+1} JSON content does not match expected.\nFound: {parsed}\nExpected: {expected}"

def test_cronjob_configured():
    """Verify that the cronjob was correctly installed."""
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True,
            check=True
        )
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run 'crontab -l'. The cronjob might not be set up.")

    expected_cron = "30 2 * * * /home/user/parser /home/user/locales.csv /home/user/processed_locales.jsonl"

    found = False
    for line in crontab_output.splitlines():
        # Remove extra whitespace to make the check robust
        normalized_line = " ".join(line.strip().split())
        normalized_expected = " ".join(expected_cron.split())
        if normalized_expected in normalized_line:
            found = True
            break

    assert found, f"Expected cronjob not found in crontab. Expected to find:\n{expected_cron}"