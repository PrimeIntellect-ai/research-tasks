# test_final_state.py
import os

def test_diagnostic_report_exists_and_correct():
    report_path = "/home/user/diagnostic_report.txt"

    assert os.path.isfile(report_path), f"The diagnostic report was not found at {report_path}. Ensure the script ran successfully."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "Synced UTC Time: 2023-10-27 10:00:00"

    assert content == expected_content, (
        f"The content of {report_path} is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Got: '{content}'"
    )