# test_final_state.py

import os
import subprocess
import pytest

REPO_DIR = "/home/user/pipeline_repo"
OUTPUT_TXT = os.path.join(REPO_DIR, "output.txt")
INIT_SQL = os.path.join(REPO_DIR, "init.sql")
PROCESS_SH = os.path.join(REPO_DIR, "process.sh")

def test_init_sql_fixed():
    """Verify that the SQL dump has been fixed."""
    assert os.path.isfile(INIT_SQL), f"{INIT_SQL} is missing."
    with open(INIT_SQL, 'r') as f:
        content = f.read()
    assert "INZERT" not in content, "init.sql still contains the corrupted 'INZERT' syntax."
    assert "INSERT INTO metrics" in content, "init.sql does not contain valid 'INSERT' statements."

def test_process_sh_syntax_fixed():
    """Verify that the bash script no longer has syntax errors."""
    assert os.path.isfile(PROCESS_SH), f"{PROCESS_SH} is missing."
    result = subprocess.run(["bash", "-n", PROCESS_SH], capture_output=True, text=True)
    assert result.returncode == 0, f"process.sh still has syntax errors:\n{result.stderr}"

def test_output_txt_correct():
    """Verify that the pipeline ran successfully and produced the correct output."""
    assert os.path.isfile(OUTPUT_TXT), f"{OUTPUT_TXT} was not generated. Did the script run successfully?"
    with open(OUTPUT_TXT, 'r') as f:
        content = f.read().strip()
    expected_output = "revenue|9984.50"
    assert content == expected_output, f"output.txt contains incorrect data. Expected '{expected_output}', got '{content}'."