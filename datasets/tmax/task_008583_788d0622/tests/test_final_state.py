# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"

def write_varint(val):
    res = b''
    while True:
        towrite = val & 0x7f
        val >>= 7
        if val:
            res += bytes([towrite | 0x80])
        else:
            res += bytes([towrite])
            break
    return res

def encode_string(field_num, s):
    header = (field_num << 3) | 2
    return write_varint(header) + write_varint(len(s)) + s.encode('utf-8')

def encode_int32(field_num, val):
    header = (field_num << 3) | 0
    return write_varint(header) + write_varint(val)

def generate_payload(filename, wid, cpu, mem, deps):
    with open(filename, 'wb') as f:
        f.write(encode_string(1, wid))
        f.write(encode_int32(2, cpu))
        f.write(encode_int32(3, mem))
        for d in deps:
            f.write(encode_string(4, d))

@pytest.fixture(scope="session", autouse=True)
def setup_and_build():
    build_script = os.path.join(WORKSPACE_DIR, "build.sh")
    assert os.path.isfile(build_script), f"Build script {build_script} not found."
    assert os.access(build_script, os.X_OK), f"Build script {build_script} is not executable."

    # Run build script
    result = subprocess.run(["bash", "build.sh"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"build.sh failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    validator_exe = os.path.join(WORKSPACE_DIR, "validator")
    assert os.path.isfile(validator_exe), "Executable 'validator' was not created by the build script."

    # Generate test payloads
    generate_payload(os.path.join(WORKSPACE_DIR, 'test_pass.bin'), 'job-123', 4, 1024, ['nginx', 'mysql', 'redis'])
    generate_payload(os.path.join(WORKSPACE_DIR, 'test_fail_cpu.bin'), 'job-124', 16, 1024, ['mysql', 'redis'])
    generate_payload(os.path.join(WORKSPACE_DIR, 'test_fail_deps.bin'), 'job-125', 2, 512, ['mysql', 'postgres'])
    generate_payload(os.path.join(WORKSPACE_DIR, 'test_fail_mem.bin'), 'job-126', 4, 4096, ['mysql', 'redis'])

def run_validator_and_check(payload_name, expected_log):
    validator_exe = os.path.join(WORKSPACE_DIR, "validator")
    payload_path = os.path.join(WORKSPACE_DIR, payload_name)
    log_path = os.path.join(WORKSPACE_DIR, "validation.log")

    if os.path.exists(log_path):
        os.remove(log_path)

    result = subprocess.run([validator_exe, payload_path], cwd=WORKSPACE_DIR, capture_output=True, text=True)

    assert os.path.isfile(log_path), "validation.log was not created."

    with open(log_path, 'r') as f:
        log_content = f.read().strip()

    assert expected_log in log_content, f"Expected '{expected_log}' in validation.log, but got '{log_content}'"

def test_pass_case():
    run_validator_and_check('test_pass.bin', 'Workload job-123 verification: PASS')

def test_fail_cpu_case():
    run_validator_and_check('test_fail_cpu.bin', 'Workload job-124 verification: FAIL')

def test_fail_deps_case():
    run_validator_and_check('test_fail_deps.bin', 'Workload job-125 verification: FAIL')

def test_fail_mem_case():
    run_validator_and_check('test_fail_mem.bin', 'Workload job-126 verification: FAIL')