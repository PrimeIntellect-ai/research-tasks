# test_final_state.py
import os
import urllib.request
import subprocess
import random

def test_symlink_created():
    symlink_path = '/home/user/www'
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"
    target = os.readlink(symlink_path)
    assert target == '/app/static' or os.path.abspath(os.path.join(os.path.dirname(symlink_path), target)) == '/app/static', \
        f"{symlink_path} does not point to /app/static"

def test_nginx_serving_static():
    static_file_path = '/app/static/index.html'
    assert os.path.exists(static_file_path), f"{static_file_path} is missing"
    with open(static_file_path, 'r') as f:
        expected_content = f.read().strip()

    try:
        response = urllib.request.urlopen("http://localhost:8080/index.html", timeout=5)
        actual_content = response.read().decode('utf-8').strip()
    except Exception as e:
        assert False, f"Failed to fetch http://localhost:8080/index.html: {e}"

    assert actual_content == expected_content, "Content served by Nginx does not match the static file"

def test_fuzz_equivalence_process_log():
    agent_script = '/home/user/process_log.py'
    oracle_script = '/app/oracle_process_log.py'

    assert os.path.exists(agent_script), f"{agent_script} does not exist"
    assert os.path.exists(oracle_script), f"{oracle_script} does not exist"

    random.seed(42)
    methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    paths = ["/api/data", "/login", "/index.html", "/images/logo.png", "/about", "/"]

    for _ in range(100):
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
        method = random.choice(methods)
        path = random.choice(paths)
        status = random.randint(200, 599)
        size = random.randint(0, 10000)
        day = random.randint(1, 28)

        log_line = f'{ip} - - [{day:02d}/Oct/2023:14:00:00 -0700] "{method} {path} HTTP/1.1" {status} {size}'

        agent_result = subprocess.run(["python3", agent_script, log_line], capture_output=True, text=True)
        oracle_result = subprocess.run(["python3", oracle_script, log_line], capture_output=True, text=True)

        assert agent_result.returncode == 0, f"Agent script failed on input: {log_line}\nStderr: {agent_result.stderr}"

        agent_output = agent_result.stdout.strip()
        oracle_output = oracle_result.stdout.strip()

        assert agent_output == oracle_output, \
            f"Output mismatch for input: {log_line}\nExpected (Oracle): {oracle_output}\nGot (Agent): {agent_output}"