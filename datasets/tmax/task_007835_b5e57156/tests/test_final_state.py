# test_final_state.py

import os
import pytest

def test_quarantined_files_exist():
    quarantine_dir = "/home/user/quarantine"
    expected_files = ["bin-00002.dat", "bin-00004.dat"]

    for f in expected_files:
        path = os.path.join(quarantine_dir, f)
        assert os.path.isfile(path), f"Expected quarantined file {path} is missing."

def test_quarantined_files_removed_from_artifacts():
    artifacts_dir = "/home/user/artifacts"
    removed_files = ["bin-00002.dat", "bin-00004.dat"]

    for f in removed_files:
        path = os.path.join(artifacts_dir, f)
        assert not os.path.exists(path), f"Quarantined file {path} should have been moved, but it still exists in the artifacts directory."

def test_other_artifacts_remain():
    artifacts_dir = "/home/user/artifacts"
    remaining_files = ["bin-00001.dat", "bin-00003.dat", "bin-00005.dat"]

    for f in remaining_files:
        path = os.path.join(artifacts_dir, f)
        assert os.path.isfile(path), f"Artifact file {path} should not have been moved."

def test_report_content():
    report_path = "/home/user/quarantine_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "bin-00002\nbin-00004"
    assert content == expected_content, f"Report content is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_no_tmp_files_left_behind():
    tmp_report_path = "/home/user/quarantine_report.txt.tmp"
    assert not os.path.exists(tmp_report_path), f"Temporary file {tmp_report_path} was left behind."