# test_final_state.py
import os

def test_deadlock_report():
    report_path = "/home/user/deadlock_report.txt"
    assert os.path.isfile(report_path), f"The report file {report_path} was not created."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected = "Deadlock IDs: 30,40,50,60,70\nTotal Cost: 1500"

    assert content == expected, (
        f"The content of {report_path} is incorrect.\n"
        f"Expected:\n{expected}\n\n"
        f"Got:\n{content}"
    )