# test_final_state.py
import os

def test_bashrc_exports():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"File missing: {bashrc_path}"

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert "export SG_USER=admin" in content, "export SG_USER=admin is missing from .bashrc"
    assert "export SG_PASS=secret123" in content, "export SG_PASS=secret123 is missing from .bashrc"

def test_success_log():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"File missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "[SUCCESS] 10.0.1.0/24 via 192.168.1.254",
        "[SUCCESS] 172.16.0.0/16 via 192.168.1.254",
        "[SUCCESS] 192.168.100.0/24 via 10.0.0.1"
    ]

    assert content == expected, f"success.log content does not match expected output.\nExpected:\n{expected}\nGot:\n{content}"

def test_scripts_exist_and_executable():
    scripts = [
        "/home/user/auto-sg.exp",
        "/home/user/diagnose.sh"
    ]

    for script in scripts:
        assert os.path.isfile(script), f"Script is missing: {script}"
        assert os.access(script, os.X_OK), f"Script is not executable: {script}"