# test_final_state.py

import os
import pytest

def test_process_log_exists_and_content():
    log_path = "/home/user/process.log"
    assert os.path.isfile(log_path), f"Missing file: {log_path}"

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == "Records processed: 9", f"Incorrect content in {log_path}. Expected 'Records processed: 9', got '{content}'"

def test_report_txt_exists_and_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Missing file: {report_path}"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_blocks = [
        "Store: Café Paris (ID: 101)\nMonth: jan_2023 -> Sales: 1500",
        "Store: Café Paris (ID: 101)\nMonth: feb_2023 -> Sales: 1650",
        "Store: Café Paris (ID: 101)\nMonth: mar_2023 -> Sales: 1800",
        "Store: El Niño Tacos (ID: 102)\nMonth: jan_2023 -> Sales: 2200",
        "Store: El Niño Tacos (ID: 102)\nMonth: feb_2023 -> Sales: 2100",
        "Store: El Niño Tacos (ID: 102)\nMonth: mar_2023 -> Sales: 2300",
        "Store: München Bratwurst (ID: 103)\nMonth: jan_2023 -> Sales: 1800",
        "Store: München Bratwurst (ID: 103)\nMonth: feb_2023 -> Sales: 1900",
        "Store: München Bratwurst (ID: 103)\nMonth: mar_2023 -> Sales: 1850"
    ]

    # Split the content by double newlines to get individual blocks
    # Handle possible trailing newlines or varying whitespace between blocks slightly
    blocks = [block.strip() for block in content.split("\n\n") if block.strip()]

    assert len(blocks) == 9, f"Expected 9 records in {report_path}, found {len(blocks)}"

    for i, expected_block in enumerate(expected_blocks):
        assert blocks[i] == expected_block, f"Record {i+1} mismatch.\nExpected:\n{expected_block}\nGot:\n{blocks[i]}"

    # Check that there is exactly one blank line between records.
    # We can do this by checking if the original content contains the exact joined string
    joined_expected = "\n\n".join(expected_blocks)
    assert joined_expected in content, "The spacing between records in report.txt is incorrect. Expected exactly one blank line between rendered record blocks."