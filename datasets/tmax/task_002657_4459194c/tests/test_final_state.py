# test_final_state.py
import os
import pytest

def test_cpp_file_exists_and_uses_mmap():
    """Verify that the C++ source file exists and uses mmap."""
    cpp_path = "/home/user/process.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file missing at {cpp_path}"

    with open(cpp_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "mmap" in content, "The C++ program must use memory-mapped I/O (mmap)."

def test_csv_output_exists():
    """Verify that the output CSV file exists."""
    csv_path = "/home/user/high_values.csv"
    assert os.path.isfile(csv_path), f"Output CSV file missing at {csv_path}"

def test_csv_contents():
    """Verify that the output CSV contains the correct header and records."""
    csv_path = "/home/user/high_values.csv"
    if not os.path.isfile(csv_path):
        pytest.fail(f"File {csv_path} does not exist.")

    with open(csv_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "The CSV file is empty."
    assert lines[0] == "id,timestamp,value", "The CSV header is incorrect."

    expected_lines = ["id,timestamp,value"]
    for i in range(800, 1000):
        val = float(i * 0.1)
        expected_lines.append(f"{i},{1600000000 + i},{val:.2f}")

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1}: expected '{expected}', got '{actual}'"