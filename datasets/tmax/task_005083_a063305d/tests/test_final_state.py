# test_final_state.py

import os
import pytest

def test_anonymized_logs():
    """Test that the anonymized_logs.csv file exists and contains the correct data."""
    log_file = "/home/user/anonymized_logs.csv"
    assert os.path.isfile(log_file), f"The file {log_file} does not exist. Did the pipeline run?"

    expected_content = """100,U01,192.168.*.*,150
105,U01,192.168.*.*,150
110,U01,192.168.*.*,200
101,U02,10.0.*.*,0
106,U02,10.0.*.*,300
100,U03,172.16.*.*,500
108,U03,172.16.*.*,500
115,U03,172.16.*.*,500
102,U04,8.8.*.*,400
103,U04,8.8.*.*,200
104,U04,1.1.*.*,200"""

    with open(log_file, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of {log_file} is incorrect. Expected masked IPs and correctly imputed response times."

def test_top_users():
    """Test that the top_users.txt file exists and contains the correct data."""
    top_users_file = "/home/user/top_users.txt"
    assert os.path.isfile(top_users_file), f"The file {top_users_file} does not exist."

    expected_content = """U03,500.00
U04,266.67
U01,166.67"""

    with open(top_users_file, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of {top_users_file} is incorrect. Expected top 3 users by average response time."

def test_scripts_exist():
    """Test that the requested source files were created."""
    c_script = "/home/user/process_logs.c"
    bash_script = "/home/user/run_pipeline.sh"

    assert os.path.isfile(c_script), f"The C program {c_script} does not exist."
    assert os.path.isfile(bash_script), f"The bash script {bash_script} does not exist."
    assert os.access(bash_script, os.X_OK), f"The bash script {bash_script} is not executable."