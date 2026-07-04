# test_final_state.py

import os
from pathlib import Path

def test_success_log_exists_and_correct():
    success_log = Path("/home/user/success.log")
    assert success_log.is_file(), "The file /home/user/success.log does not exist. Did the program run successfully?"

    content = success_log.read_text().strip()
    assert "Processing complete." in content, f"Expected 'Processing complete.' in success.log, but found: {content}"

def test_env_file_fixed():
    env_file = Path("/home/user/analyzer/.env")
    assert env_file.is_file(), "/home/user/analyzer/.env does not exist."

    content = env_file.read_text()
    assert "tcp.port == 80" in content, "The PCAP_FILTER in .env is not correctly set to 'tcp.port == 80'."

def test_main_rs_fixed():
    main_rs = Path("/home/user/analyzer/src/main.rs")
    assert main_rs.is_file(), "/home/user/analyzer/src/main.rs does not exist."

    content = main_rs.read_text()

    # The original buggy line: let cmd = format!("tshark -r {} -Y '{}' -w /tmp/filtered.pcap", filename, filter);
    # Check that the exact unquoted format string is no longer present.
    buggy_pattern = 'tshark -r {} -Y'
    assert buggy_pattern not in content, "The Rust code still contains the unquoted filename bug ('tshark -r {} -Y')."