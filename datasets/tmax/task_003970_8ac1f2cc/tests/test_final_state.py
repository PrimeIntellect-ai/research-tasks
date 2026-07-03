# test_final_state.py

import os
import stat
import hashlib
import pytest

ORIGINAL_LOGD_C = """#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    FILE *fp = fopen("/home/user/web.log", "r");
    if (!fp) {
        perror("Failed to open log file");
        return 1;
    }

    char line[512];
    while (fgets(line, sizeof(line), fp)) {
        line[strcspn(line, "\n")] = 0;

        // Only process ERROR logs
        if (strstr(line, "ERROR")) {
            char cmd[1024];
            // VULNERABILITY: Command Injection via unsanitized input
            sprintf(cmd, "echo '%s' >> /home/user/alerts.log", line);
            system(cmd);
        }
    }

    fclose(fp);
    return 0;
}
"""

def get_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def test_report_contents():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 3, f"Expected exactly 3 lines in report.txt, found {len(lines)}."

    # Line 1: Attacker IP
    assert lines[0] == "198.51.100.44", f"Line 1 of report.txt should be '198.51.100.44', got '{lines[0]}'."

    # Line 2: Original SHA256
    expected_original_sha256 = get_sha256(ORIGINAL_LOGD_C.encode('utf-8'))
    assert lines[1] == expected_original_sha256, f"Line 2 of report.txt should be the SHA256 of the original logd.c."

    # Line 3: Patched SHA256
    c_file_path = "/home/user/logd.c"
    assert os.path.isfile(c_file_path), f"Patched source file {c_file_path} is missing."
    with open(c_file_path, "rb") as f:
        current_c_content = f.read()
    expected_patched_sha256 = get_sha256(current_c_content)

    assert lines[2] == expected_patched_sha256, f"Line 3 of report.txt should be the SHA256 of the patched logd.c."

def test_remediation_script():
    script_path = "/home/user/remediation.sh"
    assert os.path.isfile(script_path), f"Remediation script {script_path} is missing."

    # Check executable permission
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Remediation script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read().strip()

    # Ignore shebang if present
    lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
    assert len(lines) == 1, "remediation.sh should contain exactly one command line."

    expected_cmd = "iptables -A INPUT -s 198.51.100.44 -p tcp -j DROP"
    assert lines[0] == expected_cmd, f"remediation.sh does not contain the correct iptables command. Got: {lines[0]}"

def test_logd_c_patched():
    c_file_path = "/home/user/logd.c"
    assert os.path.isfile(c_file_path), f"Source file {c_file_path} is missing."

    with open(c_file_path, "r") as f:
        content = f.read()

    assert "system(" not in content, "logd.c still contains 'system(' calls."
    assert "popen(" not in content, "logd.c still contains 'popen(' calls."
    assert "fopen" in content or "open(" in content, "logd.c should use secure file I/O functions."

def test_logd_fixed_executable():
    bin_path = "/home/user/logd_fixed"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."

    # Check executable permission
    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Compiled binary {bin_path} is not executable."

    # Check if it's an ELF file
    with open(bin_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{bin_path} is not a valid ELF binary."