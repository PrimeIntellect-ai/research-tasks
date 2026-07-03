# test_final_state.py

import os
import pytest

def test_script_exists():
    """Test that the bash script was created."""
    script_path = "/home/user/check_ingress.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_good_manifest_remains():
    """Test that the good manifest remains in the manifests directory."""
    good_yaml = "/home/user/k8s-operator/manifests/app-good.yaml"
    assert os.path.isfile(good_yaml), f"File {good_yaml} should still exist in the manifests directory."

def test_bad_manifest_moved():
    """Test that the bad manifest was moved to the quarantine directory."""
    bad_yaml_orig = "/home/user/k8s-operator/manifests/app-bad.yaml"
    bad_yaml_quarantine = "/home/user/k8s-operator/quarantine/app-bad.yaml"

    assert not os.path.isfile(bad_yaml_orig), f"File {bad_yaml_orig} should have been moved out of the manifests directory."
    assert os.path.isfile(bad_yaml_quarantine), f"File {bad_yaml_quarantine} should exist in the quarantine directory."

def test_dns_failures_log():
    """Test that the bad domain was logged to dns_failures.log."""
    log_file = "/home/user/k8s-operator/alerts/dns_failures.log"
    assert os.path.isfile(log_file), f"Log file {log_file} was not created."

    with open(log_file, 'r') as f:
        content = f.read().strip().split('\n')

    assert "definitely.invalid.domain.local.999" in content, f"Expected domain not found in {log_file}."

def test_mail_config_updated():
    """Test that the mail config file was updated with ALERT_TRIGGERED=1."""
    mail_config = "/home/user/k8s-operator/mail_config.rc"
    assert os.path.isfile(mail_config), f"File {mail_config} is missing."

    with open(mail_config, 'r') as f:
        content = f.read()

    assert "ALERT_TRIGGERED=1" in content, f"Expected 'ALERT_TRIGGERED=1' to be appended to {mail_config}."