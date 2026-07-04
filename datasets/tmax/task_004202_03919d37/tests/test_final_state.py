# test_final_state.py
import os
import subprocess
import stat
import re
import tempfile
import datetime

def test_deploy_script_exists_and_executable():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist."
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable."

def test_deploy_script_runs_successfully():
    deploy_script = "/home/user/deploy.sh"
    # Run it once
    result1 = subprocess.run([deploy_script], capture_output=True)
    assert result1.returncode == 0, f"{deploy_script} failed on first run: {result1.stderr.decode()}"

    # Run it twice for idempotency
    result2 = subprocess.run([deploy_script], capture_output=True)
    assert result2.returncode == 0, f"{deploy_script} failed on second run (not idempotent): {result2.stderr.decode()}"

def test_mail_spool_permissions():
    mail_spool = "/home/user/alerts/mail_spool"
    assert os.path.isdir(mail_spool), f"{mail_spool} directory does not exist."

    st = os.stat(mail_spool)
    # Check permissions 700 (drwx------)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"{mail_spool} permissions are {oct(perms)}, expected 0o700."

def test_systemd_unit_file():
    unit_file = "/home/user/.config/systemd/user/app-monitor.service"
    assert os.path.isfile(unit_file), f"{unit_file} does not exist."

    with open(unit_file, "r") as f:
        content = f.read()

    assert "Restart=always" in content, "Missing 'Restart=always' in unit file."
    assert "RestartSec=3" in content, "Missing 'RestartSec=3' in unit file."
    assert "TZ=Asia/Tokyo" in content, "Missing TZ=Asia/Tokyo environment variable in unit file."
    assert "ExecStart=/home/user/monitor_bin /home/user/app.log /home/user/alerts/mail_spool/alerts.eml" in content, \
        "ExecStart line does not match the required format."

def test_monitor_bin_logic():
    monitor_bin = "/home/user/monitor_bin"
    assert os.path.isfile(monitor_bin), f"{monitor_bin} was not compiled."
    assert os.access(monitor_bin, os.X_OK), f"{monitor_bin} is not executable."

    # Create a dummy log file
    log_content = """INFO system starting
REJECT key_auth
DEBUG connecting
REJECT key_auth
ERROR unknown
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as log_file:
        log_file.write(log_content)
        log_path = log_file.name

    out_path = log_path + "_out.eml"
    if os.path.exists(out_path):
        os.remove(out_path)

    # Run the monitor binary with TZ=Asia/Tokyo
    env = os.environ.copy()
    env["TZ"] = "Asia/Tokyo"

    result = subprocess.run([monitor_bin, log_path, out_path], env=env, capture_output=True)
    assert result.returncode == 0, f"{monitor_bin} failed to execute."

    assert os.path.isfile(out_path), "Output alert file was not created."

    with open(out_path, "r") as f:
        out_content = f.read()

    # We expect exactly two email snippets
    snippets = out_content.strip().split("Auth failure detected.")
    # The split will produce 3 parts if there are 2 snippets
    assert len(snippets) == 3, "Expected exactly 2 'Auth failure detected.' messages in the output."

    # Check the format of the first snippet
    snippet1 = snippets[0].strip()

    assert "To: admin@localhost" in snippet1, "Missing 'To: admin@localhost'"
    assert "Subject: Alert - Auth Rejected" in snippet1, "Missing 'Subject: Alert - Auth Rejected'"

    # Check date format Date: YYYY-MM-DD HH:MM:SS
    date_match = re.search(r"Date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", snippet1)
    assert date_match is not None, "Date format is incorrect or missing."

    # Cleanup
    os.remove(log_path)
    os.remove(out_path)