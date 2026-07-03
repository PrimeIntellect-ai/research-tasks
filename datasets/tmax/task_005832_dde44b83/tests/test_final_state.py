# test_final_state.py

import os
import re
import subprocess

def test_api_key_extracted():
    mem_file = "/home/user/app/crash_mem.bin"
    assert os.path.isfile(mem_file), f"The memory dump file {mem_file} is missing."

    with open(mem_file, "rb") as f:
        content = f.read()

    # Dynamically find the expected key from the binary file
    match = re.search(b"API_KEY=([a-zA-Z0-9]{16})", content)
    assert match is not None, "Could not find API_KEY in crash_mem.bin"
    expected_key = match.group(1).decode("utf-8")

    solution_file = "/home/user/solution/api_key.txt"
    assert os.path.isfile(solution_file), f"Solution file {solution_file} was not created."

    with open(solution_file, "r", encoding="utf-8") as f:
        actual_key = f.read().strip()

    assert actual_key == expected_key, f"Expected API key '{expected_key}', but found '{actual_key}' in {solution_file}"

def test_report_py_fixed():
    report_file = "/home/user/app/report.py"
    assert os.path.isfile(report_file), f"The Python script {report_file} is missing."

    with open(report_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "math.isclose" in content, "The report.py file does not appear to use math.isclose() as requested."

    # Run the script and check output
    result = subprocess.run(["python3", report_file], capture_output=True, text=True)

    assert result.returncode == 0, f"report.py crashed or returned non-zero exit code: {result.stderr}"

    output = result.stdout.strip()
    assert output == "REPORT_VALID", f"Expected script to output 'REPORT_VALID', but got '{output}'"