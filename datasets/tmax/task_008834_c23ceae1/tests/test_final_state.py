# test_final_state.py

import os
import configparser

def test_results_log():
    log_path = "/home/user/config_manager/results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist"

    with open(log_path, "r") as f:
        content = f.read().splitlines()

    expected_lines = [
        "Corrupted: serverC_corrupted.tar.gz",
        "Processed: serverA - ApprovedCommit: def5678",
        "Processed: serverB - ApprovedCommit: z111111"
    ]

    for expected in expected_lines:
        assert expected in content, f"Expected line '{expected}' not found in results.log"

def test_extracted_serverA_app_conf():
    conf_path = "/home/user/config_manager/extracted/serverA/app.conf"
    assert os.path.isfile(conf_path), f"Extracted config {conf_path} does not exist"

    with open(conf_path, "r") as f:
        content = f.read()

    legacy_count = content.count("192.168.1.100")
    new_count = content.count("10.200.50.5")

    assert legacy_count == 0, f"Expected 0 occurrences of 192.168.1.100 in serverA/app.conf, found {legacy_count}"
    assert new_count == 501, f"Expected 501 occurrences of 10.200.50.5 in serverA/app.conf, found {new_count}"

def test_extracted_serverB_app_conf():
    conf_path = "/home/user/config_manager/extracted/serverB/app.conf"
    assert os.path.isfile(conf_path), f"Extracted config {conf_path} does not exist"

    with open(conf_path, "r") as f:
        content = f.read()

    legacy_count = content.count("192.168.1.100")
    new_count = content.count("10.200.50.5")

    assert legacy_count == 0, f"Expected 0 occurrences of 192.168.1.100 in serverB/app.conf, found {legacy_count}"
    assert new_count == 201, f"Expected 201 occurrences of 10.200.50.5 in serverB/app.conf, found {new_count}"

def test_rules_ini_unchanged():
    rules_path = "/home/user/config_manager/rules.ini"
    assert os.path.isfile(rules_path), f"{rules_path} does not exist"

    config = configparser.ConfigParser()
    config.read(rules_path)

    assert config.has_section("Network"), "rules.ini missing [Network] section"
    assert config.get("Network", "legacy_ip") == "192.168.1.100", "legacy_ip modified in rules.ini"
    assert config.get("Network", "new_ip") == "10.200.50.5", "new_ip modified in rules.ini"