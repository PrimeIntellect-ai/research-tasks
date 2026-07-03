# test_final_state.py

import os
import stat
import json
import pytest

CONFIG_DIR = "/home/user/qemu_configs"
REPORT_FILE = "/home/user/hardening_report.json"

def test_vnc_password_fixed():
    """Check that password=off was replaced with password=on in the relevant files."""
    vnc_files = ["vm_web.sh", "vm_test.sh"]
    for filename in vnc_files:
        filepath = os.path.join(CONFIG_DIR, filename)
        assert os.path.isfile(filepath), f"File {filepath} is missing."
        with open(filepath, 'r') as f:
            content = f.read()
        assert "password=on" in content, f"File {filepath} does not contain 'password=on'."
        assert "password=off" not in content, f"File {filepath} still contains 'password=off'."

def test_permissions_fixed():
    """Check that world-writable files were changed to 750."""
    fixed_files = ["vm_web.sh", "vm_test.sh", "vm_safe.sh"]
    for filename in fixed_files:
        filepath = os.path.join(CONFIG_DIR, filename)
        assert os.path.isfile(filepath), f"File {filepath} is missing."
        st = os.stat(filepath)
        actual_perms = stat.S_IMODE(st.st_mode)
        assert actual_perms == 0o750, f"File {filepath} has permissions {oct(actual_perms)}, expected 0o750."

def test_unaffected_files():
    """Check that files not needing fixes were left unchanged."""
    filepath = os.path.join(CONFIG_DIR, "vm_db.sh")
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    st = os.stat(filepath)
    actual_perms = stat.S_IMODE(st.st_mode)
    assert actual_perms == 0o644, f"File {filepath} has permissions {oct(actual_perms)}, expected 0o644."

    with open(filepath, 'r') as f:
        content = f.read()
    assert "password=on" in content, f"File {filepath} does not contain 'password=on'."
    assert "password=off" not in content, f"File {filepath} contains 'password=off'."

def test_hardening_report():
    """Check that the hardening report is generated correctly."""
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} was not generated."

    with open(REPORT_FILE, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {REPORT_FILE} is not valid JSON.")

    assert "vnc_fixed" in report, "Report is missing 'vnc_fixed' key."
    assert "permissions_fixed" in report, "Report is missing 'permissions_fixed' key."

    expected_vnc_fixed = ["vm_test.sh", "vm_web.sh"]
    expected_perms_fixed = ["vm_safe.sh", "vm_test.sh", "vm_web.sh"]

    assert sorted(report["vnc_fixed"]) == expected_vnc_fixed, \
        f"Expected vnc_fixed to be {expected_vnc_fixed}, got {report['vnc_fixed']}."

    assert sorted(report["permissions_fixed"]) == expected_perms_fixed, \
        f"Expected permissions_fixed to be {expected_perms_fixed}, got {report['permissions_fixed']}."