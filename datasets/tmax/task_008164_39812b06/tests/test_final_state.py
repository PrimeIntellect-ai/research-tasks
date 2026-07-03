# test_final_state.py
import os
import subprocess

def test_binaries_exist():
    assert os.path.isfile('/home/user/build/auth_x86'), "auth_x86 binary is missing. Did the Makefile compile it?"
    assert os.path.isfile('/home/user/build/auth_arm'), "auth_arm binary is missing. Did the Makefile compile it?"

def test_binaries_architecture():
    # Check x86 binary
    try:
        out_x86 = subprocess.check_output(['file', '/home/user/build/auth_x86']).decode('utf-8')
        assert 'x86-64' in out_x86 or '80386' in out_x86 or 'ELF 64-bit LSB' in out_x86, "auth_x86 does not appear to be an x86 ELF binary."
    except FileNotFoundError:
        # Fallback if 'file' command is not available, we can use readelf
        out_x86 = subprocess.check_output(['readelf', '-h', '/home/user/build/auth_x86']).decode('utf-8')
        assert 'X86-64' in out_x86 or '80386' in out_x86, "auth_x86 does not appear to be an x86 ELF binary."

    # Check ARM binary
    try:
        out_arm = subprocess.check_output(['file', '/home/user/build/auth_arm']).decode('utf-8')
        assert 'aarch64' in out_arm or 'ARM' in out_arm, "auth_arm does not appear to be an ARM ELF binary."
    except FileNotFoundError:
        out_arm = subprocess.check_output(['readelf', '-h', '/home/user/build/auth_arm']).decode('utf-8')
        assert 'AArch64' in out_arm or 'ARM' in out_arm, "auth_arm does not appear to be an ARM ELF binary."

def test_security_violations_log():
    log_path = '/home/user/build/security_violations.log'
    assert os.path.isfile(log_path), f"The file {log_path} is missing."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}."
    assert lines[0] == 'websec_debug_bypass', f"Expected 'websec_debug_bypass' on line 1, found '{lines[0]}'."
    assert lines[1] == 'websec_debug_bypass', f"Expected 'websec_debug_bypass' on line 2, found '{lines[1]}'."