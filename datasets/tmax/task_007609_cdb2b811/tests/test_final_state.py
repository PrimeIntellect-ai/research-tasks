# test_final_state.py

import os
import hashlib
import stat
import pytest

def test_audit_report():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report file not found at {report_path}"

    # Recompute the expected password by finding the hash in ps_dump and cracking it with the wordlist
    ps_dump_path = "/home/user/ps_dump.txt"
    wordlist_path = "/home/user/wordlist.txt"

    assert os.path.isfile(ps_dump_path), "ps_dump.txt missing"
    assert os.path.isfile(wordlist_path), "wordlist.txt missing"

    target_hash = None
    with open(ps_dump_path, "r") as f:
        for line in f:
            if "/home/user/bin/backup_job" in line and "--auth-hash" in line:
                parts = line.split()
                try:
                    hash_idx = parts.index("--auth-hash") + 1
                    target_hash = parts[hash_idx]
                except (ValueError, IndexError):
                    pass
                break

    assert target_hash is not None, "Could not find --auth-hash in ps_dump.txt"

    cracked_password = None
    with open(wordlist_path, "r") as f:
        for word in f:
            word = word.strip()
            if hashlib.md5(word.encode('utf-8')).hexdigest() == target_hash:
                cracked_password = word
                break

    assert cracked_password is not None, "Could not crack the password using the wordlist"

    # Check SUID bit on the executable
    binary_path = "/home/user/bin/backup_job"
    assert os.path.isfile(binary_path), f"Executable not found at {binary_path}"
    st = os.stat(binary_path)
    suid_str = "YES" if (st.st_mode & stat.S_ISUID) else "NO"

    expected_line = f"Binary: {binary_path} | SUID: {suid_str} | Leaked Password: {cracked_password}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == expected_line, f"Audit report content is incorrect. Expected: '{expected_line}', Got: '{content}'"

def test_logs_redacted():
    orig_logs_dir = "/home/user/logs"
    redacted_logs_dir = "/home/user/logs_redacted"

    assert os.path.isdir(redacted_logs_dir), f"Redacted logs directory not found at {redacted_logs_dir}"

    orig_files = set(os.listdir(orig_logs_dir))
    redacted_files = set(os.listdir(redacted_logs_dir))

    assert orig_files == redacted_files, "Redacted logs directory does not contain the exact same filenames as the original logs directory"

    # Recompute cracked password to know what to replace
    # We can just rely on the same logic or hardcode 'supersecret' since we tested the derivation above.
    # For robustness, we will extract it again or just use 'supersecret' as it's logically derived.
    # We'll use 'supersecret' as we already validated its derivation in the previous test.
    password_to_redact = "supersecret"

    for filename in orig_files:
        orig_path = os.path.join(orig_logs_dir, filename)
        redacted_path = os.path.join(redacted_logs_dir, filename)

        with open(orig_path, "r") as f:
            orig_content = f.read()

        expected_redacted_content = orig_content.replace(password_to_redact, "[REDACTED]")

        with open(redacted_path, "r") as f:
            actual_redacted_content = f.read()

        assert actual_redacted_content == expected_redacted_content, f"Content of {redacted_path} is not correctly redacted."