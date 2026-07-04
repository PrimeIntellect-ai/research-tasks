# test_final_state.py
import os
import subprocess
import re
import pytest

def test_anomaly_report():
    gen_log = "/home/user/logs/generator.log"
    assert os.path.exists(gen_log), f"{gen_log} is missing"

    with open(gen_log, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 74, "generator.log does not have enough lines to find the anomaly."

    # The anomaly is at line 74 (index 73)
    line_74 = lines[73].strip()
    match = re.match(r"\[(.*?)\] Generated value: (.*)", line_74)
    assert match, "Line 74 in generator.log is not in the expected format."

    timestamp = match.group(1)
    value = match.group(2)

    report_file = "/home/user/anomaly_report.txt"
    assert os.path.exists(report_file), f"{report_file} is missing. You need to create the report."

    with open(report_file, "r") as f:
        report_content = f.read().strip()

    expected_report = f"Timestamp: {timestamp}, Value: {value}"
    assert report_content == expected_report, (
        f"anomaly_report.txt content is incorrect.\n"
        f"Expected: '{expected_report}'\n"
        f"Got: '{report_content}'"
    )

def test_build_success():
    build_script = "/home/user/build.sh"
    assert os.path.exists(build_script), f"{build_script} is missing"

    result = subprocess.run([build_script], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"build.sh failed with exit code {result.returncode}.\n"
        f"Stdout:\n{result.stdout}\n"
        f"Stderr:\n{result.stderr}"
    )

def test_output_txt():
    output_file = "/home/user/output.txt"
    assert os.path.exists(output_file), f"{output_file} is missing. Did the processor script run?"

    with open(output_file, "r") as f:
        lines = f.read().splitlines()

    data_file = "/home/user/data.txt"
    assert os.path.exists(data_file), f"{data_file} is missing."
    with open(data_file, "r") as f:
        data_lines = f.read().splitlines()

    assert len(lines) == len(data_lines), (
        f"output.txt has {len(lines)} lines, but data.txt has {len(data_lines)}. "
        f"The processor should output exactly one line per input line."
    )

    invalid_count = 0
    for i, line in enumerate(lines):
        if line == "INVALID":
            invalid_count += 1
            assert float(data_lines[i]) < 0, f"Line {i+1} in output.txt is INVALID, but input data was {data_lines[i]} (not negative)."
        else:
            try:
                float(line)
            except ValueError:
                pytest.fail(f"Line {i+1} in output.txt is not a valid number or 'INVALID': {line}")

    assert invalid_count == 1, f"Expected exactly 1 'INVALID' in output.txt, but found {invalid_count}."