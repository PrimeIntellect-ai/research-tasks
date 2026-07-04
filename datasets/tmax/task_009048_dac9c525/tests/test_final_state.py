# test_final_state.py

import os
import stat
import re

def test_fix_app_script_exists_and_executable():
    script_path = "/home/user/fix_app.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"Script {script_path} is not executable."

def test_nginx_conf_updated():
    conf_path = "/home/user/app/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    expected_directive = "proxy_pass http://unix:/home/user/app/run/gunicorn.sock;"
    assert expected_directive in content, f"Nginx config does not contain the corrected proxy_pass directive: {expected_directive}"

    # Check for idempotency / no duplicates
    count = content.count("proxy_pass")
    assert count == 1, "Nginx config contains multiple proxy_pass directives, suggesting the script is not idempotent."

def test_failed_sockets_txt():
    output_path = "/home/user/failed_sockets.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/app/gunicorn.sock",
        "/home/user/app/tmp/gunicorn.sock"
    ]

    assert lines == expected_lines, f"Contents of {output_path} are incorrect. Expected {expected_lines}, got {lines}."

def test_port_forward_sh():
    script_path = "/home/user/port_forward.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read().strip()

    # Check for key tokens in iptables command
    required_tokens = [
        "iptables",
        "-t", "nat",
        "PREROUTING",
        "-i", "eth0",
        "-p", "tcp",
        "80",
        "REDIRECT",
        "8080"
    ]

    # We can split by whitespace and check if tokens are present, or just check substrings.
    # Since some might be combined like `--dport 80` or `--to-port 8080`

    assert "iptables" in content, "iptables command missing 'iptables'"
    assert "-t nat" in content, "iptables command missing '-t nat'"
    assert "PREROUTING" in content, "iptables command missing 'PREROUTING'"
    assert "-i eth0" in content, "iptables command missing '-i eth0'"
    assert "-p tcp" in content, "iptables command missing '-p tcp'"
    assert "80" in content, "iptables command missing port '80'"
    assert "REDIRECT" in content, "iptables command missing 'REDIRECT'"
    assert "8080" in content, "iptables command missing port '8080'"

    # Check that it's just a single line (ignoring shebang if present)
    lines = [line for line in content.split("\n") if line.strip() and not line.startswith("#")]
    assert len(lines) == 1, f"File {script_path} should contain exactly one iptables command line."