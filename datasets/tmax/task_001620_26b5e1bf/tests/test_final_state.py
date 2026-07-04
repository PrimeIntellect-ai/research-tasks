# test_final_state.py

import os
import subprocess
import difflib
import pytest

def test_target_txt_correct():
    target_path = "/app/target.txt"
    assert os.path.isfile(target_path), f"Missing target file: {target_path}"

    with open(target_path, 'r') as f:
        content = f.read().strip()

    expected_path = "/root/.ssh/authorized_keys"
    assert content == expected_path, f"Expected '{expected_path}' in {target_path}, but got '{content}'"

def test_server_fixed_binary_exists():
    binary_path = "/app/server_fixed"
    assert os.path.isfile(binary_path), f"Missing compiled binary: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

def test_server_c_logic():
    server_c_path = "/app/server.c"
    assert os.path.isfile(server_c_path), f"Missing source code: {server_c_path}"

    with open(server_c_path, 'r') as f:
        src = f.read()

    # Rename the student's main function so we can compile our own test harness
    src_modified = src.replace("int main", "int student_main")

    harness = """
#include <stdio.h>
#include <stdlib.h>

int handle_upload(const char* filename, const char* content);

int main() {
    // Ensure uploads directory exists for the normal test
    system("mkdir -p /app/uploads");

    int res1 = handle_upload("../evil.txt", "bad");
    int res2 = handle_upload("/etc/evil.txt", "bad");
    int res3 = handle_upload("good.txt", "good");

    if (res1 != -1) return 1; // Failed to reject ../
    if (res2 != -1) return 2; // Failed to reject /
    if (res3 != 0) return 3;  // Failed to accept normal file

    return 0;
}
"""
    test_src_path = "/tmp/test_server.c"
    test_bin_path = "/tmp/test_server"

    with open(test_src_path, 'w') as f:
        f.write(src_modified + "\n" + harness)

    compile_res = subprocess.run(["gcc", "-o", test_bin_path, test_src_path], capture_output=True, text=True)
    assert compile_res.returncode == 0, f"Failed to compile test harness with server.c:\n{compile_res.stderr}"

    run_res = subprocess.run([test_bin_path])
    if run_res.returncode == 1:
        pytest.fail("server.c handle_upload did not reject filename containing '../'")
    elif run_res.returncode == 2:
        pytest.fail("server.c handle_upload did not reject filename starting with '/'")
    elif run_res.returncode == 3:
        pytest.fail("server.c handle_upload rejected a valid filename")
    elif run_res.returncode != 0:
        pytest.fail(f"server.c handle_upload test harness failed with exit code {run_res.returncode}")

def test_redact_sh_accuracy():
    script_path = "/app/redact.sh"
    eval_log = "/app/secret_eval.log"
    golden_log = "/app/secret_eval_golden.log"

    assert os.path.isfile(script_path), f"Missing redaction script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Redaction script is not executable: {script_path}"

    result = subprocess.run([script_path, eval_log], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed to execute properly.\nStderr: {result.stderr}"

    agent_out = result.stdout

    with open(golden_log, 'r') as f:
        golden_out = f.read()

    matcher = difflib.SequenceMatcher(None, agent_out, golden_out)
    accuracy = matcher.ratio()

    assert accuracy >= 0.95, f"Redaction accuracy {accuracy:.4f} is below the threshold of 0.95"