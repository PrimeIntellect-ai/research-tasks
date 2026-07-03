# test_final_state.py

import os
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.exists(script_path), f"Pipeline script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Pipeline script is not executable: {script_path}"

def test_cpp_source_exists():
    cpp_path = '/home/user/process_configs.cpp'
    assert os.path.exists(cpp_path), f"C++ source file missing: {cpp_path}"

def test_reports_directory_exists():
    reports_dir = '/home/user/reports'
    assert os.path.exists(reports_dir), f"Reports directory missing: {reports_dir}"
    assert os.path.isdir(reports_dir), f"Reports path is not a directory: {reports_dir}"

def test_us_east_report_content():
    report_path = '/home/user/reports/region_US-East.txt'
    assert os.path.exists(report_path), f"Report file missing: {report_path}"

    expected_content = (
        "Server: S1\n"
        "IP: 10.0.0.XXX\n"
        "Admin: ad***@company.com\n"
        "Changed MaxConnections to 100 by U***5 at 2023-10-01T10:00:00Z\n"
        "---\n"
        "Server: S1\n"
        "IP: 10.0.0.XXX\n"
        "Admin: ad***@company.com\n"
        "Changed Port to 8080 by U***5 at 2023-10-02T09:00:00Z\n"
        "---\n"
    )

    with open(report_path, 'r') as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content mismatch in {report_path}"

def test_eu_west_report_content():
    report_path = '/home/user/reports/region_EU-West.txt'
    assert os.path.exists(report_path), f"Report file missing: {report_path}"

    expected_content = (
        "Server: S2\n"
        "IP: 192.168.100.XXX\n"
        "Admin: sy***@company.com\n"
        "Changed Timeout to 30 by U***5 at 2023-10-01T11:00:00Z\n"
        "---\n"
        "Server: S2\n"
        "IP: 192.168.100.XXX\n"
        "Admin: sy***@company.com\n"
        "Changed SSL to true by U***5 at 2023-10-04T14:20:00Z\n"
        "---\n"
    )

    with open(report_path, 'r') as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content mismatch in {report_path}"

def test_us_west_report_content():
    report_path = '/home/user/reports/region_US-West.txt'
    assert os.path.exists(report_path), f"Report file missing: {report_path}"

    expected_content = (
        "Server: S3\n"
        "IP: 172.16.5.XXX\n"
        "Admin: de***@internal.net\n"
        "Changed LogLevel to DEBUG by A***Z at 2023-10-03T08:15:00Z\n"
        "---\n"
    )

    with open(report_path, 'r') as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content mismatch in {report_path}"