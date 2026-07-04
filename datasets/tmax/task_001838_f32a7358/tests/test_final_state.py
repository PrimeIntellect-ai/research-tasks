# test_final_state.py
import os
import subprocess
import csv

def get_interpreter(binary_path):
    try:
        output = subprocess.check_output(["readelf", "-l", binary_path], stderr=subprocess.DEVNULL).decode('utf-8')
        for line in output.splitlines():
            if "program interpreter" in line:
                # Example line: [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
                parts = line.split(":")
                if len(parts) > 1:
                    return parts[1].strip().strip("]")
    except Exception:
        pass
    return None

def test_csv_exists():
    csv_path = "/home/user/elf_deps.csv"
    assert os.path.isfile(csv_path), f"The output CSV file {csv_path} was not created."

def test_csv_content():
    csv_path = "/home/user/elf_deps.csv"
    assert os.path.isfile(csv_path), "CSV file missing."

    ls_interp = get_interpreter("/bin/ls")
    cat_interp = get_interpreter("/bin/cat")

    assert ls_interp is not None, "Could not determine interpreter for /bin/ls"
    assert cat_interp is not None, "Could not determine interpreter for /bin/cat"

    expected_rows = [
        ["job-101", "/home/user/bin/app_ls", ls_interp],
        ["job-103", "/home/user/bin/app_cat", cat_interp]
    ]

    actual_rows = []
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # skip empty lines
                actual_rows.append(row)

    assert len(actual_rows) == 2, f"Expected exactly 2 lines in the CSV, but found {len(actual_rows)}."

    # Verify that the expected rows are present (order might not be strictly enforced, but usually is)
    for expected_row in expected_rows:
        assert expected_row in actual_rows, f"Expected row {expected_row} not found in the CSV. Actual contents: {actual_rows}"

def test_script_exists():
    script_path = "/home/user/tracker.sh"
    assert os.path.isfile(script_path), f"The Bash script {script_path} was not created."