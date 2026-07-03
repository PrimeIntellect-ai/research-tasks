# test_final_state.py

import os
import re

PROJECT_DIR = "/home/user/project"

def test_success_log_output():
    log_path = os.path.join(PROJECT_DIR, "success.log")
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did you run the app and redirect output?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert "Result: 35" in content, f"Expected 'Result: 35' in {log_path}, but got: {content}"

def test_build_artifacts_exist():
    app_path = os.path.join(PROJECT_DIR, "app")
    lib_path = os.path.join(PROJECT_DIR, "libmathops.so")

    assert os.path.isfile(app_path), f"Executable {app_path} is missing. Did build.py run successfully?"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} is missing."

def test_hypothesis_test_file():
    test_path = os.path.join(PROJECT_DIR, "test_semver.py")
    assert os.path.isfile(test_path), f"Test file {test_path} is missing."

    with open(test_path, 'r') as f:
        content = f.read()

    assert "hypothesis" in content, "The test file does not seem to import or use 'hypothesis'."
    assert "@given" in content or "given(" in content, "The test file does not seem to use the @given decorator from hypothesis."

    # Check for some logic representing anti-symmetry or symmetry property
    # It should call compare_versions(v1, v2) and compare_versions(v2, v1)
    assert "compare_versions" in content, "The test file does not call compare_versions."

    # We can use a simple regex to see if both orders are called or if it's generally checking the property
    matches = re.findall(r'compare_versions\s*\(', content)
    assert len(matches) >= 1, "Expected compare_versions to be used in the hypothesis test."

def test_sym_emulator_fixed():
    sym_path = os.path.join(PROJECT_DIR, "sym_emulator.py")
    assert os.path.isfile(sym_path), f"File {sym_path} is missing."

    with open(sym_path, 'r') as f:
        content = f.read()

    # The bug was "pass" under "elif state == 'WEAK_RESOLVED':"
    # It should now transition to STRONG_RESOLVED if sym_type == 'STRONG'
    assert "STRONG_RESOLVED" in content, "sym_emulator.py doesn't seem to contain STRONG_RESOLVED transitions."
    assert "pass" not in content.split("elif state == 'WEAK_RESOLVED':")[-1].split("elif")[0], "sym_emulator.py still seems to have the missing transition (pass) for WEAK_RESOLVED."