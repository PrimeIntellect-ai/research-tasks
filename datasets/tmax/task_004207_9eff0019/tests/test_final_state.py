# test_final_state.py
import os
import subprocess
import random
import string
import re

def test_processor_fuzz_equivalence():
    oracle = "/app/oracle_processor"
    agent_prog = "/home/user/bin/processor"

    assert os.path.isfile(agent_prog), f"Agent program {agent_prog} is missing."
    assert os.access(agent_prog, os.X_OK), f"Agent program {agent_prog} is not executable."

    random.seed(42)
    # Exclude characters that might cause shell/argument parsing issues if not handled,
    # but since we pass via subprocess list, printable is mostly fine.
    # We'll use standard printable ASCII minus some whitespace just to be safe.
    chars = string.ascii_letters + string.digits + string.punctuation + " "

    for _ in range(100):
        length = random.randint(1, 100)
        inp = "".join(random.choice(chars) for _ in range(length))

        oracle_res = subprocess.run([oracle, inp], capture_output=True, text=True, errors='replace')
        agent_res = subprocess.run([agent_prog, inp], capture_output=True, text=True, errors='replace')

        assert oracle_res.stdout == agent_res.stdout, (
            f"Output mismatch on input {inp!r}.\n"
            f"Oracle output: {oracle_res.stdout!r}\n"
            f"Agent output: {agent_res.stdout!r}"
        )

def test_nginx_config_fixed():
    conf_path = "/home/user/nginx/conf/nginx.conf"
    assert os.path.isfile(conf_path), f"{conf_path} is missing."
    with open(conf_path, "r") as f:
        content = f.read()

    assert "fastcgi_pass 127.0.0.1:9000;" in content, "nginx.conf does not contain the fixed fastcgi_pass port 9000."
    assert "9099" not in content, "nginx.conf still contains the broken port 9099."

def test_logrotate_config():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"{conf_path} is missing."
    with open(conf_path, "r") as f:
        content = f.read()

    # Check for the correct log path
    assert "/home/user/nginx/logs/" in content and ".log" in content, "Logrotate config does not target the correct log files (e.g. /home/user/nginx/logs/*.log)."

    # Check directives
    directives = ["daily", "rotate 7", "compress", "missingok"]
    for d in directives:
        assert re.search(r'\b' + d.replace(' ', r'\s+') + r'\b', content), f"Logrotate config does not specify '{d}'."