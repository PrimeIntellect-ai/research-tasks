# test_final_state.py
import os
import subprocess
import re

BASE_DIR = "/home/user/malware_analysis"

def test_requirements_fixed():
    req_path = os.path.join(BASE_DIR, "requirements.txt")
    assert os.path.isfile(req_path), f"{req_path} is missing."
    with open(req_path, "r") as f:
        content = f.read()
    # requests==2.26.0 requires urllib3<1.27,>=1.21.1
    # Check that urllib3==1.20 is not present if requests==2.26.0 is there.
    if "requests==2.26.0" in content:
        assert "urllib3==1.20" not in content, "requirements.txt still contains conflicting urllib3==1.20"

def test_parser_fixed():
    parser_path = os.path.join(BASE_DIR, "parser.py")
    assert os.path.isfile(parser_path), f"{parser_path} is missing."
    with open(parser_path, "r") as f:
        content = f.read()

    # Check that data[0] is guarded or length is checked
    assert re.search(r'if\s+length\s*>\s*0', content) or re.search(r'if\s+len\(data\)\s*>\s*0', content) or re.search(r'if\s+not\s+data', content) or "continue" in content or "data[0]" not in content or re.search(r'if\s+data:', content), "parser.py does not seem to guard against length=0 or empty data."

def test_cluster_beacons_fixed():
    c_path = os.path.join(BASE_DIR, "cluster_beacons.c")
    assert os.path.isfile(c_path), f"{c_path} is missing."
    with open(c_path, "r") as f:
        content = f.read()

    # Check that division by zero is guarded
    assert re.search(r'if\s*\(\s*counts\[k\]\s*>\s*0\s*\)', content) or re.search(r'counts\[k\]\s*!=\s*0', content) or re.search(r'counts\[k\]\s*==\s*0', content), "cluster_beacons.c does not seem to guard against division by zero (counts[k] == 0)."

def test_regression_test_sh():
    script_path = os.path.join(BASE_DIR, "regression_test.sh")
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Run the script and check output
    result = subprocess.run([script_path], cwd=BASE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"regression_test.sh failed with exit code {result.returncode}"
    assert "REGRESSION TEST PASSED" in result.stdout, "regression_test.sh did not print 'REGRESSION TEST PASSED'"

def test_final_beacons_output():
    final_path = os.path.join(BASE_DIR, "final_beacons.txt")
    assert os.path.isfile(final_path), f"{final_path} is missing. Did you run the pipeline?"

    with open(final_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Centroids:",
        "13.00",
        "51.00"
    ]

    lines = [line.strip() for line in content.split("\n") if line.strip()]
    assert lines == expected_lines, f"final_beacons.txt content is incorrect. Expected {expected_lines}, got {lines}"