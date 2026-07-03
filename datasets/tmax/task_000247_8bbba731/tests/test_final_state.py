# test_final_state.py

import os
import re
import pytest

def get_dir_size(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
    return total

def test_scripts_exist_and_executable():
    scripts = [
        "/home/user/storage_optimizer.sh",
        "/home/user/run_finops_pipeline.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_staging_environment_state():
    staging_artifacts = "/home/user/staging_artifacts"
    staging_archive = "/home/user/staging_archive"

    assert os.path.isdir(staging_archive), f"Directory {staging_archive} was not created."

    # Check archived files
    archived_file = os.path.join(staging_archive, "build_1.tar.gz")
    assert os.path.isfile(archived_file), f"File {archived_file} was not archived."

    # Check remaining files
    for filename in ["build_2.tar.gz", "build_3.tar.gz"]:
        filepath = os.path.join(staging_artifacts, filename)
        assert os.path.isfile(filepath), f"File {filepath} should not have been archived."

    # Check directory size
    total_size = get_dir_size(staging_artifacts)
    assert total_size == 52428800, f"Staging artifacts directory size is {total_size}, expected 52428800."

def test_prod_environment_state():
    prod_artifacts = "/home/user/prod_artifacts"
    prod_archive = "/home/user/prod_archive"

    assert os.path.isdir(prod_archive), f"Directory {prod_archive} was not created."

    # Check archived files
    for filename in ["log_old.log", "log_mid.log"]:
        archived_file = os.path.join(prod_archive, filename)
        assert os.path.isfile(archived_file), f"File {archived_file} was not archived."

    # Check remaining files
    for filename in ["app_v1.jar", "app_v2.jar"]:
        filepath = os.path.join(prod_artifacts, filename)
        assert os.path.isfile(filepath), f"File {filepath} should not have been archived."

    # Check directory size
    total_size = get_dir_size(prod_artifacts)
    assert total_size == 41943040, f"Prod artifacts directory size is {total_size}, expected 41943040."

def test_prod_finops_csv_report():
    report_file = "/home/user/prod_finops.csv"
    assert os.path.isfile(report_file), f"Report file {report_file} does not exist."

    with open(report_file, "r") as f:
        content = f.read().strip()

    lines = [line for line in content.split("\n") if line.strip()]

    # There should be at least two lines containing the archived files.
    # (Allowing for an optional header line)

    log_old_pattern = re.compile(r"^\d+,log_old\.log,41943040,/home/user/prod_artifacts,/home/user/prod_archive$")
    log_mid_pattern = re.compile(r"^\d+,log_mid\.log,20971520,/home/user/prod_artifacts,/home/user/prod_archive$")

    found_log_old = any(log_old_pattern.match(line) for line in lines)
    found_log_mid = any(log_mid_pattern.match(line) for line in lines)

    assert found_log_old, f"Report {report_file} missing or incorrect entry for log_old.log."
    assert found_log_mid, f"Report {report_file} missing or incorrect entry for log_mid.log."