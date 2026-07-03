# test_final_state.py
import os
import subprocess
import random
import string
import base64
import tempfile
import shutil

def generate_payload(syscalls: str, xor_key: int = 0x5A) -> bytes:
    encrypted = bytes([ord(c) ^ xor_key for c in syscalls])
    return base64.b64encode(encrypted)

def create_test_binary(base_source: str, temp_dir: str, name: str, payload: bytes = None):
    source_path = os.path.join(temp_dir, f"{name}.c")
    base_bin = os.path.join(temp_dir, f"{name}_base")
    final_bin = os.path.join(temp_dir, name)

    with open(source_path, "w") as f:
        f.write(base_source)

    subprocess.run(["gcc", "-static", source_path, "-o", base_bin], check=True)

    if payload is not None:
        payload_path = os.path.join(temp_dir, f"{name}_payload.bin")
        with open(payload_path, "wb") as f:
            f.write(payload)
        subprocess.run(["objcopy", "--add-section", f".secpolicy={payload_path}", base_bin, final_bin], check=True)
    else:
        shutil.copy(base_bin, final_bin)

    return final_bin

def test_secure_runner_equivalence():
    agent_bin = "/home/user/secure_runner"
    oracle_bin = "/opt/oracle/secure_runner_oracle"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable"

    base_source = """
    #include <unistd.h>
    #include <string.h>
    int main(int argc, char **argv) {
        if (argc > 1) {
            write(1, argv[1], strlen(argv[1]));
            write(1, "\\n", 1);
        }
        return 0;
    }
    """

    random.seed(42)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a few different binaries
        binaries = []

        # 1. Valid payload with enough syscalls
        valid_syscalls = "execve,write,exit_group,brk,arch_prctl,uname,readlink"
        binaries.append(create_test_binary(base_source, temp_dir, "bin_valid", generate_payload(valid_syscalls)))

        # 2. Valid payload but missing 'write' (should be killed by seccomp when it tries to write)
        missing_write_syscalls = "execve,exit_group,brk,arch_prctl,uname,readlink"
        binaries.append(create_test_binary(base_source, temp_dir, "bin_missing_write", generate_payload(missing_write_syscalls)))

        # 3. Invalid XOR key
        binaries.append(create_test_binary(base_source, temp_dir, "bin_bad_xor", generate_payload(valid_syscalls, xor_key=0x11)))

        # 4. Invalid base64
        binaries.append(create_test_binary(base_source, temp_dir, "bin_bad_b64", b"NOT_BASE64_!@#"))

        # 5. Missing .secpolicy section
        binaries.append(create_test_binary(base_source, temp_dir, "bin_missing_secpolicy", None))

        for i in range(100):
            test_bin = random.choice(binaries)
            arg_len = random.randint(1, 64)
            arg = "".join(random.choices(string.ascii_letters + string.digits, k=arg_len))

            agent_cmd = [agent_bin, test_bin, arg]
            oracle_cmd = [oracle_bin, test_bin, arg]

            agent_res = subprocess.run(agent_cmd, capture_output=True)
            oracle_res = subprocess.run(oracle_cmd, capture_output=True)

            assert agent_res.returncode == oracle_res.returncode, (
                f"Mismatch on iteration {i} for binary {os.path.basename(test_bin)}.\n"
                f"Arg: {arg}\n"
                f"Oracle exit code: {oracle_res.returncode}, Agent exit code: {agent_res.returncode}\n"
                f"Oracle stdout: {oracle_res.stdout}\nAgent stdout: {agent_res.stdout}\n"
                f"Oracle stderr: {oracle_res.stderr}\nAgent stderr: {agent_res.stderr}"
            )

            assert agent_res.stdout == oracle_res.stdout, (
                f"Mismatch on iteration {i} for binary {os.path.basename(test_bin)}.\n"
                f"Arg: {arg}\n"
                f"Oracle stdout: {oracle_res.stdout}\nAgent stdout: {agent_res.stdout}"
            )