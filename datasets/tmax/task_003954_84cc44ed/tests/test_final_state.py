# test_final_state.py
import os
import re
import socket
import subprocess
import random
import string
import tempfile
import shutil
import pytest

def oracle_converter(input_str):
    output = []
    for line in input_str.splitlines():
        if line.startswith("COMMIT:"):
            output.append(f"TRANSACTION START {line[7:]}")
        elif line.startswith("AUTHOR:"):
            output.append(f"SET_USER {line[7:]}")
        else:
            m = re.match(r"^([AMD])\s+(.+)$", line)
            if m:
                op = m.group(1)
                filename = m.group(2)
                if op == 'A':
                    output.append(f"FILE_ADD {filename}")
                elif op == 'M':
                    output.append(f"FILE_MOD {filename}")
                elif op == 'D':
                    output.append(f"FILE_DEL {filename}")

    if not output:
        return ""
    return "\n".join(output) + "\n"

def generate_fuzz_input(seed):
    random.seed(seed)
    lines = []
    for _ in range(random.randint(5, 20)):
        choice = random.choice(['COMMIT', 'AUTHOR', 'AMD', 'GARBAGE', 'BLANK'])
        if choice == 'COMMIT':
            h = ''.join(random.choices("0123456789abcdef", k=random.randint(6, 40)))
            lines.append(f"COMMIT:{h}")
        elif choice == 'AUTHOR':
            name = ''.join(random.choices(string.ascii_letters + " ", k=random.randint(3, 15)))
            lines.append(f"AUTHOR:{name}")
        elif choice == 'AMD':
            op = random.choice(['A', 'M', 'D'])
            fname = ''.join(random.choices(string.ascii_letters + "._", k=random.randint(5, 15)))
            lines.append(f"{op}\t{fname}")
            lines.append(f"{op}       {fname}")
        elif choice == 'GARBAGE':
            garbage = ''.join(random.choices(string.printable, k=random.randint(5, 20))).replace('\n', '')
            lines.append(garbage)
        elif choice == 'BLANK':
            lines.append("")
    return "\n".join(lines) + "\n"

def test_fuzz_protocol_converter():
    agent_script = "/home/user/protocol_converter.py"
    assert os.path.isfile(agent_script), f"{agent_script} is missing."

    for i in range(100):
        input_data = generate_fuzz_input(i)

        expected_output = oracle_converter(input_data)

        proc = subprocess.run(
            ["python3", agent_script],
            input=input_data.encode('utf-8'),
            capture_output=True
        )

        assert proc.returncode == 0, f"Script failed on input:\n{input_data}\nError:\n{proc.stderr.decode()}"

        actual_output = proc.stdout.decode('utf-8')
        assert actual_output == expected_output, f"Mismatch on input:\n{input_data}\nExpected:\n{expected_output}\nActual:\n{actual_output}"

def test_proxy_running():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', 9999))
    sock.close()
    assert result == 0, "Proxy is not listening on localhost:9999."

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"{conf_path} is missing."

    with open(conf_path, 'r') as f:
        content = f.read()

    assert re.search(r'\bdaily\b', content), "logrotate.conf missing 'daily'"
    assert re.search(r'\brotate\s+5\b', content), "logrotate.conf missing 'rotate 5'"
    assert re.search(r'\bcompress\b', content), "logrotate.conf missing 'compress'"
    assert re.search(r'\bnotifempty\b', content), "logrotate.conf missing 'notifempty'"

def test_end_to_end_git_push():
    central_repo = "/home/user/central.git"
    assert os.path.isdir(central_repo), f"{central_repo} is missing."

    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(["git", "clone", central_repo, tmpdir], check=True, capture_output=True)

        test_file = os.path.join(tmpdir, "test_file.txt")
        with open(test_file, "w") as f:
            f.write("test content\n")

        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)
        subprocess.run(["git", "add", "test_file.txt"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "add test file"], cwd=tmpdir, check=True)

        proc_push = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True)
        assert proc_push.returncode == 0, f"Git push failed: {proc_push.stderr.decode()}"

        log_file = "/home/user/logs/legacy_sync.log"
        assert os.path.isfile(log_file), f"{log_file} is missing after push."

        with open(log_file, 'r') as f:
            log_content = f.read()

        assert "LOGIN:" in log_content, "Log missing LOGIN prompt"
        assert "PASSWORD:" in log_content, "Log missing PASSWORD prompt"
        assert "READY>" in log_content, "Log missing READY prompt"
        assert "TRANSACTION START" in log_content, "Log missing TRANSACTION START"
        assert "SET_USER Test User" in log_content, "Log missing SET_USER"
        assert "FILE_ADD test_file.txt" in log_content, "Log missing FILE_ADD"
        assert "LOGOUT" in log_content, "Log missing LOGOUT"