# test_final_state.py

import os
import pytest
from decimal import Decimal

def test_fixed_report_exists_and_correct():
    report_path = "/home/user/fixed_report.txt"
    assert os.path.exists(report_path), f"File {report_path} is missing."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, 'r') as f:
        content = f.read().strip()

    # Recompute the expected value to be robust
    total_time = Decimal('86400000.0')
    downtime = Decimal('300.1') + Decimal('100.2') + Decimal('50.15')
    sla = Decimal('100.0') - ((downtime / total_time) * Decimal('100.0'))
    expected_sla = round(sla, 6)
    expected_content = f"SLA: {expected_sla:.6f}%"

    assert content == expected_content, f"Expected report content to be '{expected_content}', but got '{content}'."

def test_uptime_monitor_exists():
    script_path = "/home/user/uptime_monitor.py"
    assert os.path.exists(script_path), f"File {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."