# test_final_state.py

import os
import subprocess
import sys
import importlib.util
import pytest

def test_phase1_auth_token():
    token_path = "/home/user/auth_token.txt"
    assert os.path.exists(token_path), f"Missing auth token file at {token_path}"

    with open(token_path, "r") as f:
        content = f.read().strip()

    expected_token = "AUTH_TOKEN: 9F8A-7B6C-5D4E-3F2A"
    assert content == expected_token, f"Token mismatch. Expected '{expected_token}', got '{content}'"

def test_phase2_build_script():
    build_script = "/home/user/build.sh"
    assert os.path.exists(build_script), f"Missing build script at {build_script}"
    assert os.access(build_script, os.X_OK), f"Build script at {build_script} is not executable"

    # Run the build script
    result = subprocess.run([build_script], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"Build script failed with return code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    debug_so = "/home/user/libcalc_debug.so"
    release_so = "/home/user/libcalc_release.so"

    assert os.path.exists(debug_so), f"Missing debug shared library at {debug_so}"
    assert os.path.exists(release_so), f"Missing release shared library at {release_so}"

    # Check for debug symbols using readelf
    readelf_debug = subprocess.run(["readelf", "-S", debug_so], capture_output=True, text=True)
    assert ".debug_info" in readelf_debug.stdout, f"Debug symbols missing in {debug_so}"

    readelf_release = subprocess.run(["readelf", "-S", release_so], capture_output=True, text=True)
    assert ".debug_info" not in readelf_release.stdout, f"Debug symbols inappropriately present in {release_so}"

def test_phase3_sanitizer_corpus():
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.exists(sanitizer_path), f"Missing sanitizer module at {sanitizer_path}"

    # Load the module
    spec = importlib.util.spec_from_file_location("sanitizer", sanitizer_path)
    sanitizer = importlib.util.module_from_spec(spec)
    sys.modules["sanitizer"] = sanitizer
    try:
        spec.loader.exec_module(sanitizer)
    except Exception as e:
        pytest.fail(f"Failed to load sanitizer.py: {e}")

    assert hasattr(sanitizer, "is_safe_expression"), "is_safe_expression function missing in sanitizer.py"

    clean_corpus_path = "/app/corpus/clean"
    evil_corpus_path = "/app/corpus/evil"

    assert os.path.exists(clean_corpus_path), f"Clean corpus missing at {clean_corpus_path}"
    assert os.path.exists(evil_corpus_path), f"Evil corpus missing at {evil_corpus_path}"

    clean_files = [f for f in os.listdir(clean_corpus_path) if os.path.isfile(os.path.join(clean_corpus_path, f))]
    evil_files = [f for f in os.listdir(evil_corpus_path) if os.path.isfile(os.path.join(evil_corpus_path, f))]

    clean_failures = []
    evil_failures = []

    for filename in clean_files:
        filepath = os.path.join(clean_corpus_path, filename)
        with open(filepath, "r") as f:
            expr = f.read().strip()
        try:
            if not sanitizer.is_safe_expression(expr):
                clean_failures.append(filename)
        except Exception:
            clean_failures.append(filename)

    for filename in evil_files:
        filepath = os.path.join(evil_corpus_path, filename)
        with open(filepath, "r") as f:
            expr = f.read().strip()
        try:
            if sanitizer.is_safe_expression(expr):
                evil_failures.append(filename)
        except Exception:
            pass # Exceptions on evil strings are acceptable if they effectively reject it

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))