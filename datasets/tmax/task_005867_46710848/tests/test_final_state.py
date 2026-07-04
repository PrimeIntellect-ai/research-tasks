# test_final_state.py

import os
import sqlite3
import subprocess
import tarfile
import pytest

WAF_DIR = "/home/user/waf_project"

def test_verify_sigs_sh_exists_and_executable():
    script_path = os.path.join(WAF_DIR, "verify_sigs.sh")
    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        first_line = f.readline().strip()
    assert "bash" in first_line or "sh" in first_line, f"Script {script_path} does not appear to be a Bash/shell script."

def test_database_schema_migrated():
    db_path = os.path.join(WAF_DIR, "db", "rules.sqlite")
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(core_rules);")
    columns = cursor.fetchall()

    severity_col = None
    for col in columns:
        if col[1] == "severity":
            severity_col = col
            break

    assert severity_col is not None, "Column 'severity' is missing from 'core_rules' table."
    # PRAGMA table_info returns: (cid, name, type, notnull, dflt_value, pk)
    assert "INT" in severity_col[2].upper(), "Column 'severity' is not of type INTEGER."
    assert str(severity_col[4]) == "5", f"Column 'severity' does not have default value 5. Found: {severity_col[4]}"

    conn.close()

def test_make_release_target():
    # Clean first to ensure the target actually builds the artifacts
    subprocess.run(["make", "clean"], cwd=WAF_DIR, capture_output=True)

    # Run make release
    result = subprocess.run(["make", "release"], cwd=WAF_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"'make release' failed with error:\n{result.stderr}"

def test_build_logs_content():
    log_path = os.path.join(WAF_DIR, "build_logs.txt")
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read()

    assert "OK: rule1.conf" in content, "build_logs.txt is missing 'OK: rule1.conf'"
    assert "OK: rule2.conf" in content, "build_logs.txt is missing 'OK: rule2.conf'"
    assert "FAIL" not in content, "build_logs.txt contains unexpected FAIL messages."

def test_tarball_contents():
    tar_path = os.path.join(WAF_DIR, "waf_release.tar.gz")
    assert os.path.isfile(tar_path), f"Tarball {tar_path} was not created."

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getnames()

    # Tarball might have prefixes like ./db/rules.sqlite or just db/rules.sqlite
    # We will check if the required files end with the expected paths
    def contains_path(expected):
        return any(m.endswith(expected) for m in members)

    assert contains_path("db/rules.sqlite"), "Tarball is missing db/rules.sqlite"
    assert contains_path("downloads/rule1.conf"), "Tarball is missing downloads/rule1.conf"
    assert contains_path("downloads/rule2.conf"), "Tarball is missing downloads/rule2.conf"