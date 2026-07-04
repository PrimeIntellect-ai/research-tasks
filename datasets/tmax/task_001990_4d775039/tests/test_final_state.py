# test_final_state.py
import os

def test_drift_report_exists():
    assert os.path.isfile("/home/user/drift_report.csv"), "The file /home/user/drift_report.csv does not exist."

def test_drift_report_content():
    expected_content = (
        "Month,Previous_Month,Distance\n"
        "2023-02,2023-01,0.600\n"
        "2023-03,2023-02,0.800"
    ).strip()

    with open("/home/user/drift_report.csv", "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of /home/user/drift_report.csv does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Actual:\n{actual_content}"
    )

def test_drift_report_lines():
    with open("/home/user/drift_report.csv", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in the CSV (1 header, 2 data rows), but found {len(lines)}."
    assert lines[0] == "Month,Previous_Month,Distance", f"Header is incorrect. Found: {lines[0]}"

    # Check data rows
    row1 = lines[1].split(',')
    assert len(row1) == 3, "Row 1 does not have exactly 3 columns."
    assert row1[0] == "2023-02", f"Row 1 Month should be 2023-02, found {row1[0]}"
    assert row1[1] == "2023-01", f"Row 1 Previous_Month should be 2023-01, found {row1[1]}"
    assert row1[2] == "0.600", f"Row 1 Distance should be 0.600, found {row1[2]}"

    row2 = lines[2].split(',')
    assert len(row2) == 3, "Row 2 does not have exactly 3 columns."
    assert row2[0] == "2023-03", f"Row 2 Month should be 2023-03, found {row2[0]}"
    assert row2[1] == "2023-02", f"Row 2 Previous_Month should be 2023-02, found {row2[1]}"
    assert row2[2] == "0.800", f"Row 2 Distance should be 0.800, found {row2[2]}"