# test_final_state.py

import os
import re
import subprocess

def test_urllib3_downgraded():
    try:
        import urllib3
        assert urllib3.__version__ == "1.26.15", f"Expected urllib3 version 1.26.15, but found {urllib3.__version__}"
    except ImportError:
        # If running in a different environment, we can check via pip
        result = subprocess.run(["pip", "show", "urllib3"], capture_output=True, text=True)
        assert "Version: 1.26.15" in result.stdout, "urllib3 version 1.26.15 is not installed."

def test_parser_script_fixed():
    script_path = "/home/user/incident/parser.py"
    assert os.path.exists(script_path), f"Script {script_path} is missing."

    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"parser.py failed to run. Stderr: {result.stderr}"
    assert result.stdout.strip() == "55", f"Expected parser.py to output '55', got '{result.stdout.strip()}'"

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read()

    # Check for IP
    assert re.search(r"IP:\s*192\.168\.100\.42", content), "Report does not contain the correct IP address (192.168.100.42)."

    # Check for TOKEN
    assert re.search(r"TOKEN:\s*TOKEN-a1b2c3d4e5f67890a1b2c3d4e5f67890", content), "Report does not contain the correct TOKEN."

    # Check for CHECKSUM
    assert re.search(r"CHECKSUM:\s*55", content), "Report does not contain the correct CHECKSUM (55)."