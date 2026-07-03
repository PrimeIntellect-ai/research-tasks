# test_final_state.py

import os
import subprocess
import re
import pytest

def test_generate_payload_c_exists():
    assert os.path.isfile("/home/user/generate_payload.c"), "The file /home/user/generate_payload.c does not exist."

def test_compile_and_execute_payload():
    # Compile
    compile_proc = subprocess.run(
        ["gcc", "-o", "/home/user/generate_payload", "/home/user/generate_payload.c"],
        capture_output=True,
        text=True
    )
    assert compile_proc.returncode == 0, f"Compilation failed:\n{compile_proc.stderr}"

    assert os.path.isfile("/home/user/generate_payload"), "Compiled executable not found."

    # Execute
    run_proc = subprocess.run(
        ["/home/user/generate_payload"],
        capture_output=True,
        text=True
    )
    assert run_proc.returncode == 0, "Execution of generate_payload failed (non-zero exit code)."

    output = run_proc.stdout.strip()
    assert output, "The program produced no output."

    # 1. Check for SSH key structure
    assert output.startswith("ssh-rsa AAAAB3NzaC1yc2E"), "Output does not start with 'ssh-rsa AAAAB3NzaC1yc2E'."

    parts = output.split(" ", 2)
    assert len(parts) == 3, "Output does not have three space-separated parts (type, key, comment)."

    key_part = parts[1]
    assert len(key_part) >= 64, "The base64 key part is less than 64 characters long."

    # 2. Check for evasion constraints (no 'script' or 'onload' case-insensitive)
    lower_output = output.lower()
    assert "script" not in lower_output, "The payload contains the banned string 'script'."
    assert "onload" not in lower_output, "The payload contains the banned string 'onload'."

    # 3. Check for valid XSS executing alert('PWNED')
    assert "alert('pwned')" in lower_output or "alert('PWNED')" in output, "The payload does not contain alert('PWNED')."

    # 4. Ensure an HTML event handler or similar vector is present (since onload and script are banned)
    assert re.search(r"on[a-z]+=", output, re.IGNORECASE), "The payload does not contain an HTML event handler (e.g., onerror=)."