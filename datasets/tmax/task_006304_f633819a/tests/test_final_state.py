# test_final_state.py

import os
import json

def test_security_report_exists():
    report_path = "/home/user/security_report.json"
    assert os.path.isfile(report_path), f"The file {report_path} does not exist."

def test_security_report_content():
    report_path = "/home/user/security_report.json"
    assert os.path.isfile(report_path), f"The file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} is not valid JSON."

    assert "outdated_libs" in report, "The JSON report is missing the 'outdated_libs' key."
    assert "insecure_exports" in report, "The JSON report is missing the 'insecure_exports' key."

    expected_outdated_libs = ["libalpha.so", "libgamma.so"]
    expected_insecure_exports = ["libalpha.so"]

    assert isinstance(report["outdated_libs"], list), "'outdated_libs' should be a list."
    assert isinstance(report["insecure_exports"], list), "'insecure_exports' should be a list."

    assert sorted(report["outdated_libs"]) == expected_outdated_libs, \
        f"Expected outdated_libs to be {expected_outdated_libs}, but got {report['outdated_libs']}."

    assert sorted(report["insecure_exports"]) == expected_insecure_exports, \
        f"Expected insecure_exports to be {expected_insecure_exports}, but got {report['insecure_exports']}."