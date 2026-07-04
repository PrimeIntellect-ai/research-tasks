# test_final_state.py
import os

def test_category_totals_file_exists():
    """Check if the output file was created at the correct path."""
    assert os.path.isfile("/home/user/category_totals.txt"), "The file /home/user/category_totals.txt does not exist."

def test_category_totals_content():
    """Check if the output file contains the correct aggregated and formatted data."""
    expected_content = (
        "Clothing: 40.00\n"
        "Electronics: 400.00\n"
        "Furniture: 165.50\n"
        "Groceries: 300.00\n"
        "Toys: 70.00"
    )

    file_path = "/home/user/category_totals.txt"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of {file_path} is incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{actual_content}"
    )