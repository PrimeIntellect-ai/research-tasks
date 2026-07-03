# test_final_state.py

import os
import re
import pytest

def test_sensitive_data_redaction():
    db_config = "/home/user/app_repo/database.config"
    api_config = "/home/user/app_repo/api.config"

    for config_file in [db_config, api_config]:
        assert os.path.isfile(config_file), f"Configuration file {config_file} is missing."

        with open(config_file, "r") as f:
            content = f.read()

        assert "SECRET_TOKEN=REDACTED" in content, f"Secret token was not redacted in {config_file}."

        # Ensure no 32-character hex strings remain for SECRET_TOKEN
        hex_match = re.search(r"SECRET_TOKEN=[a-fA-F0-9]{32}", content)
        assert not hex_match, f"A 32-character hexadecimal secret token was found unredacted in {config_file}."

def test_file_integrity_verification():
    log_file = "/home/user/compromised.log"
    assert os.path.isfile(log_file), f"Compromised log file {log_file} was not created."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_path = "/home/user/app_repo/scripts/deploy.sh"
    assert len(lines) == 1, f"Expected exactly one compromised file in the log, found {len(lines)}."
    assert lines[0] == expected_path, f"Expected {expected_path} in compromised log, but found {lines[0]}."

def test_exploit_output():
    out_file = "/home/user/exploit_out.txt"
    assert os.path.isfile(out_file), f"Exploit output file {out_file} was not created."

    with open(out_file, "r") as f:
        content = f.read()

    expected_flag = "FLAG{c0mm4nd_1nj3ct10n_m4st3r}"
    assert expected_flag in content, f"The expected flag {expected_flag} was not found in the exploit output."