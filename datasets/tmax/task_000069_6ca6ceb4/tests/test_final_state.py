# test_final_state.py

import os
import pytest

def get_expected_results():
    txs = {}

    # Read Service A
    try:
        with open("/home/user/service_a.log", "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    txs[parts[1]] = {'A': int(parts[0])}
    except FileNotFoundError:
        pass

    # Read Service B
    try:
        with open("/home/user/service_b.log", "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2 and parts[1] in txs:
                    txs[parts[1]]['B'] = int(parts[0])
    except FileNotFoundError:
        pass

    # Read Service C
    try:
        with open("/home/user/service_c.log", "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2 and parts[1] in txs:
                    txs[parts[1]]['C'] = int(parts[0])
    except FileNotFoundError:
        pass

    total = len(txs)
    converged = 0
    failed = []
    violations = []

    for tx_id, times in txs.items():
        if 'A' in times and 'B' in times and 'C' in times:
            if times['A'] < times['B'] < times['C']:
                converged += 1
            else:
                violations.append(tx_id)
        else:
            failed.append(tx_id)

    failed.sort()
    violations.sort()

    failed_str = ", ".join(failed) if failed else "None"
    violations_str = ", ".join(violations) if violations else "None"

    return {
        "Total": str(total),
        "Converged": str(converged),
        "Failed": failed_str,
        "Violations": violations_str
    }

def test_report_exists():
    """Verify that the report file was created."""
    report_file = "/home/user/report.txt"
    assert os.path.exists(report_file), f"Report file {report_file} does not exist. Did you write the output?"
    assert os.path.isfile(report_file), f"{report_file} is not a file."

def test_report_content():
    """Verify the contents of the report match the expected computed values."""
    report_file = "/home/user/report.txt"
    assert os.path.exists(report_file), f"Report file {report_file} does not exist."

    expected = get_expected_results()

    parsed_report = {}
    with open(report_file, "r") as f:
        for line in f:
            if ":" in line:
                key, val = line.split(":", 1)
                parsed_report[key.strip()] = val.strip()

    assert "Total" in parsed_report, "Report is missing the 'Total' field."
    assert parsed_report["Total"] == expected["Total"], f"Expected Total: {expected['Total']}, but got: {parsed_report['Total']}"

    assert "Converged" in parsed_report, "Report is missing the 'Converged' field."
    assert parsed_report["Converged"] == expected["Converged"], f"Expected Converged: {expected['Converged']}, but got: {parsed_report['Converged']}"

    assert "Failed" in parsed_report, "Report is missing the 'Failed' field."
    assert parsed_report["Failed"] == expected["Failed"], f"Expected Failed: {expected['Failed']}, but got: {parsed_report['Failed']}"

    assert "Violations" in parsed_report, "Report is missing the 'Violations' field."
    assert parsed_report["Violations"] == expected["Violations"], f"Expected Violations: {expected['Violations']}, but got: {parsed_report['Violations']}"