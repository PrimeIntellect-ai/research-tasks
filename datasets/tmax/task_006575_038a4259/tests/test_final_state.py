# test_final_state.py

import os
import json
import subprocess
import pytest

REPORT_PATH = "/home/user/forensics_report.json"
MAL_ELF_PATH = "/tmp/mal.elf"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist. Did you create it?"

def test_report_content():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} is missing."

    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    assert "malicious_line_number" in report, "Missing 'malicious_line_number' key in the JSON report."
    assert "elf_architecture" in report, "Missing 'elf_architecture' key in the JSON report."
    assert "c2_domain" in report, "Missing 'c2_domain' key in the JSON report."

    assert report["malicious_line_number"] == 4, f"Expected malicious_line_number to be 4, got {report['malicious_line_number']}."
    assert report["c2_domain"] == "c2.evil-empire.local", f"Expected c2_domain to be 'c2.evil-empire.local', got '{report['c2_domain']}'."

    # Dynamically determine the expected architecture string
    try:
        output = subprocess.check_output(["readelf", "-h", MAL_ELF_PATH], text=True)
        machine_str = ""
        for line in output.splitlines():
            if "Machine:" in line:
                machine_str = line.split("Machine:")[1].strip()
                break
    except Exception as e:
        pytest.fail(f"Failed to execute readelf on {MAL_ELF_PATH} to determine the ground truth architecture: {e}")

    assert machine_str != "", "Could not parse the 'Machine:' string from the truth ELF file."
    assert report["elf_architecture"].strip() == machine_str, f"Expected elf_architecture to be '{machine_str}', got '{report['elf_architecture']}'."