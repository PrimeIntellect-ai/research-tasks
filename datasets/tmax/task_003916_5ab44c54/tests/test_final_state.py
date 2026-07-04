# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

AGENT_SCRIPT = "/home/user/generate_csp.sh"
ORACLE_SCRIPT = "/app/oracle_csp.sh"

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

def create_fuzz_env(base_dir):
    webroot = os.path.join(base_dir, "webroot")
    os.makedirs(webroot)

    # Create random subdirectories
    num_dirs = random.randint(0, 15)
    for _ in range(num_dirs):
        dirname = generate_random_string(random.randint(3, 12))
        dirpath = os.path.join(webroot, dirname)
        os.makedirs(dirpath)

        # Randomly set permissions
        mode = 0o755
        if random.random() < 0.3:
            mode |= 0o002 # world writable
        if random.random() < 0.3:
            mode |= 0o1000 # sticky bit

        os.chmod(dirpath, mode)

    # Create random header file
    header_file = os.path.join(base_dir, "headers.txt")
    headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html",
        f"Server: {generate_random_string()}",
        f"X-Random-Header: {generate_random_string()}"
    ]

    with open(header_file, "wb") as f:
        for h in headers:
            f.write(h.encode('utf-8') + b"\r\n")
        f.write(b"\r\n")
        f.write(b"<html><body>" + generate_random_string(20).encode('utf-8') + b"</body></html>\r\n")

    return webroot, header_file

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable"
    assert os.path.exists(ORACLE_SCRIPT), f"Oracle script not found at {ORACLE_SCRIPT}"

    random.seed(42)
    N = 100

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N):
            env_dir = os.path.join(tmpdir, f"test_{i}")
            os.makedirs(env_dir)
            webroot, header_file = create_fuzz_env(env_dir)

            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_SCRIPT, webroot, header_file],
                capture_output=True,
                text=True
            )
            oracle_out = oracle_proc.stdout

            # Run agent
            agent_proc = subprocess.run(
                [AGENT_SCRIPT, webroot, header_file],
                capture_output=True,
                text=True
            )
            agent_out = agent_proc.stdout

            if oracle_out != agent_out:
                # Provide a clear failure message
                with open(header_file, "r") as f:
                    header_content = f.read()

                dirs_info = []
                for d in os.listdir(webroot):
                    dpath = os.path.join(webroot, d)
                    if os.path.isdir(dpath):
                        perms = oct(os.stat(dpath).st_mode)[-4:]
                        dirs_info.append(f"{d}: {perms}")

                error_msg = (
                    f"Mismatch on fuzz iteration {i}.\n"
                    f"Webroot subdirectories and permissions:\n{', '.join(dirs_info)}\n\n"
                    f"Input header file content:\n{header_content}\n"
                    f"=== ORACLE OUTPUT ===\n{oracle_out}\n"
                    f"=== AGENT OUTPUT ===\n{agent_out}\n"
                )
                pytest.fail(error_msg)