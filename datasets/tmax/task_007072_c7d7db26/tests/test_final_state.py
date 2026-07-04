# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/waf-project"

def test_resolve_deps_exists_executable():
    script_path = os.path.join(PROJECT_DIR, "resolve_deps.sh")
    assert os.path.isfile(script_path), f"File {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_flags_txt_content():
    flags_path = os.path.join(PROJECT_DIR, "flags.txt")
    assert os.path.isfile(flags_path), f"File {flags_path} is missing."

    with open(flags_path, 'r') as f:
        content = f.read().strip()

    valid_flags = [
        "-lwaf -lparser -lcrypto -llog",
        "-lwaf -lcrypto -lparser -llog"
    ]

    # Allow for multiple spaces or trailing spaces
    normalized_content = " ".join(content.split())

    assert normalized_content in valid_flags, \
        f"flags.txt content '{normalized_content}' does not match expected topological sort."

def test_waf_engine_patched():
    c_file = os.path.join(PROJECT_DIR, "waf_engine.c")
    assert os.path.isfile(c_file), f"File {c_file} is missing."

    with open(c_file, 'r') as f:
        content = f.read()

    assert "insecure_func" not in content, "waf_engine.c still contains 'insecure_func', patch was not applied correctly."
    assert "secure_func" in content, "waf_engine.c does not contain 'secure_func', patch was not applied correctly."

def test_ci_fix_patch_exists():
    patch_file = os.path.join(PROJECT_DIR, "ci_fix.patch")
    assert os.path.isfile(patch_file), f"File {patch_file} is missing."

def test_build_success_log():
    log_file = os.path.join(PROJECT_DIR, "build_success.log")
    assert os.path.isfile(log_file), f"File {log_file} is missing. Did the CI pipeline run successfully?"

    with open(log_file, 'r') as f:
        content = f.read()

    assert "Secured WAF Engine Running" in content, \
        "build_success.log does not contain the expected output 'Secured WAF Engine Running'."