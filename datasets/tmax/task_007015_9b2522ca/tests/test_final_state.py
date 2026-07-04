# test_final_state.py

import os
import subprocess
import tempfile
import stat

def test_recovered_key():
    key_path = "/home/user/recovered_key.txt"
    assert os.path.isfile(key_path), f"Verification failed: {key_path} missing."

    with open(key_path, "r") as f:
        content = f.read().replace("\n", "").replace("\r", "")

    expected_key = "SECRET_KEY_99824_XOR_OBFUSCATION"
    assert content == expected_key, f"Verification failed: Incorrect recovered key. Expected '{expected_key}', got '{content}'."

def test_fuzzer_and_crash_reproduction():
    fuzzer_path = "/home/user/fuzzer.sh"
    assert os.path.isfile(fuzzer_path), f"Verification failed: {fuzzer_path} is missing."
    assert os.access(fuzzer_path, os.X_OK), f"Verification failed: {fuzzer_path} is not executable."

    # Run fuzzer
    try:
        subprocess.run([fuzzer_path], check=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Verification failed: {fuzzer_path} execution failed with exit code {e.returncode}."

    crash_input_path = "/home/user/crash_input.txt"
    assert os.path.isfile(crash_input_path), f"Verification failed: fuzzer did not create {crash_input_path}"

    original_buggy_script = """#!/bin/bash
sum=0
while IFS= read -r -n1 char; do
    if [[ -z "$char" ]]; then continue; fi
    val=$(printf "%d" "'$char")
    divisor=$(( val % 10 ))
    sum=$(( (sum + val) / divisor ))
done < "$1"
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_script:
        tmp_script.write(original_buggy_script)
        tmp_script_path = tmp_script.name

    os.chmod(tmp_script_path, os.stat(tmp_script_path).st_mode | stat.S_IEXEC)

    result = subprocess.run(
        [tmp_script_path, crash_input_path], 
        capture_output=True, 
        text=True
    )

    os.remove(tmp_script_path)

    assert "division by 0" in result.stderr.lower() or "division by zero" in result.stderr.lower(), \
        "Verification failed: crash_input.txt does not trigger division by zero in the original script."

def test_analyzer_fix():
    analyzer_path = "/home/user/analyzer.sh"
    crash_input_path = "/home/user/crash_input.txt"

    assert os.path.isfile(analyzer_path), f"Verification failed: {analyzer_path} missing."
    assert os.path.isfile(crash_input_path), f"Verification failed: {crash_input_path} missing. Fuzzer test must pass first."

    result = subprocess.run(
        [analyzer_path, crash_input_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Verification failed: analyzer.sh returned error code {result.returncode}."
    assert "division by 0" not in result.stderr.lower() and "division by zero" not in result.stderr.lower(), \
        "Verification failed: analyzer.sh still crashes with division by zero."

    with open(analyzer_path, "r") as f:
        analyzer_content = f.read()

    # Check if logic to set divisor to 1 exists
    has_fix_logic = ("divisor=1" in analyzer_content.replace(" ", "")) or ("divisor-eq0" in analyzer_content.replace(" ", "")) or ("divisor==0" in analyzer_content.replace(" ", ""))
    assert has_fix_logic, "Verification failed: logic to set divisor to 1 when 0 not found in analyzer.sh."