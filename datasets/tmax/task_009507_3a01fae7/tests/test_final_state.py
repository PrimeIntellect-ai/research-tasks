# test_final_state.py

import os
import re

def test_redacted_txt_exists_and_correct():
    path = "/home/user/redacted.txt"
    assert os.path.exists(path), f"Missing {path}"
    assert os.path.isfile(path), f"{path} is not a file"

    expected_content = (
        "Content-Security-Policy: default-src 'none';\n\n"
        "Patient records show John Doe has SSN ***-**-**** and Jane Doe has SSN ***-**-****. Do not share."
    )

    with open(path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"The contents of {path} do not match the expected output."

def test_secure_processor_c_exists_and_uses_seccomp():
    path = "/home/user/secure_processor.c"
    assert os.path.exists(path), f"Missing {path}"
    assert os.path.isfile(path), f"{path} is not a file"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for prctl call with strict seccomp
    # PR_SET_SECCOMP is 22, SECCOMP_MODE_STRICT is 1. Some might use prctl(22, 1) or prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT)
    # The prompt mentions prctl(15, 1) which is actually PR_SET_NAME? No, PR_SET_SECCOMP is 22. Wait, the prompt says "prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT) or prctl(15, 1)". (Wait, PR_SET_SECCOMP is 22 in linux headers). Let's just check for 'prctl' and 'SECCOMP' or '1'.
    has_prctl = re.search(r'prctl\s*\(', content)
    has_seccomp = re.search(r'SECCOMP_MODE_STRICT', content) or re.search(r'1', content)

    assert has_prctl, f"{path} does not seem to call prctl()"
    assert "prctl" in content, "prctl call not found in source code."

def test_secure_processor_executable_exists():
    path = "/home/user/secure_processor"
    assert os.path.exists(path), f"Missing {path}"
    assert os.path.isfile(path), f"{path} is not a file"
    assert os.access(path, os.X_OK), f"{path} is not executable"