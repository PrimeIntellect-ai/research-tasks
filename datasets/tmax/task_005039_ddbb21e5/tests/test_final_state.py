# test_final_state.py

import os
import json
import pytest

def test_service_report_json():
    """Verify the JSON report exists and has the correct content."""
    report_path = "/home/user/service_report.json"
    assert os.path.isfile(report_path), f"JSON report file {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected = {
        "svc_worker_alpha": True,
        "svc_worker_beta": False,
        "svc_worker_gamma": True
    }
    assert data == expected, f"JSON content in {report_path} does not match the expected state. Got: {data}"

def test_symlinks_created_for_running_services():
    """Verify symlinks are created for running services and point to correct directories."""
    alpha_link = "/home/user/mnt/alpha_link"
    alpha_data = "/home/user/data/alpha_data"

    assert os.path.isdir(alpha_data), f"Source directory {alpha_data} does not exist."
    assert os.path.islink(alpha_link), f"Symlink {alpha_link} does not exist or is not a symlink."
    assert os.readlink(alpha_link) == alpha_data, f"Symlink {alpha_link} does not point to {alpha_data}."

    gamma_link = "/home/user/mnt/gamma_link"
    gamma_data = "/home/user/data/gamma_data"

    assert os.path.isdir(gamma_data), f"Source directory {gamma_data} does not exist."
    assert os.path.islink(gamma_link), f"Symlink {gamma_link} does not exist or is not a symlink."
    assert os.readlink(gamma_link) == gamma_data, f"Symlink {gamma_link} does not point to {gamma_data}."

def test_symlinks_removed_for_stopped_services():
    """Verify symlinks are removed for services that are not running."""
    beta_link = "/home/user/mnt/beta_link"

    assert not os.path.exists(beta_link), f"File or symlink {beta_link} still exists, but the service is not running."
    assert not os.path.islink(beta_link), f"Symlink {beta_link} still exists, but the service is not running."