# test_final_state.py
import os
import subprocess
import random
import string

def test_nginx_config():
    conf_path = "/app/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "deny 192.168.200.0/24;" in content, "Nginx config does not contain the required deny directive: 'deny 192.168.200.0/24;'."

def generate_fuzz_input():
    length = random.randint(50, 4096)
    chars = string.ascii_letters + string.digits + " ;=-\r\n"
    res = "".join(random.choices(chars, k=length))

    # Inject interesting patterns to trigger the redaction logic
    if random.random() < 0.5:
        res = "Cookie: " + res
    elif random.random() < 0.5:
        res = "Set-Cookie: " + res

    if random.random() < 0.5:
        idx = random.randint(0, max(0, len(res) - 20))
        res = res[:idx] + "X-Auth-Exfil-Token=" + res[idx:]

    return res.encode('utf-8')

def test_redactor_fuzz_equivalence():
    oracle_path = "/app/oracle_redactor"
    agent_path = "/home/user/redactor"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    N = 5000

    for i in range(N):
        inp = generate_fuzz_input()

        oracle_proc = subprocess.run([oracle_path], input=inp, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=inp, capture_output=True)

        if oracle_proc.stdout != agent_proc.stdout:
            err_msg = (
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input (repr):\n{repr(inp)}\n"
                f"Oracle output (repr):\n{repr(oracle_proc.stdout)}\n"
                f"Agent output (repr):\n{repr(agent_proc.stdout)}\n"
            )
            assert False, err_msg