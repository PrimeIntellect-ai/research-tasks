# test_final_state.py

import os
import re

def test_update_lb_script_exists_and_executable():
    script_path = "/home/user/update_lb.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_upstream_conf_content():
    log_path = "/home/user/deployment.log"
    conf_path = "/home/user/upstream.conf"

    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    assert os.path.isfile(conf_path), f"Configuration file {conf_path} does not exist."

    # Parse log file to determine expected healthy ports
    port_status = {}
    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Example line: [2023-11-01 10:00:00] [PORT: 8081] [STATUS: IN_PROGRESS]
            match = re.search(r'\[PORT:\s*(\d+)\]\s*\[STATUS:\s*([A-Z_]+)\]', line)
            if match:
                port = int(match.group(1))
                status = match.group(2)
                port_status[port] = status

    healthy_ports = sorted([p for p, s in port_status.items() if s == "SUCCESS"])

    expected_conf_lines = ["upstream backend_cluster {"]
    for port in healthy_ports:
        expected_conf_lines.append(f"    server 127.0.0.1:{port};")
    expected_conf_lines.append("}")
    expected_conf = "\n".join(expected_conf_lines)

    with open(conf_path, 'r') as f:
        actual_conf = f.read().strip()

    assert actual_conf == expected_conf, (
        f"Content of {conf_path} does not match expected output.\n"
        f"Expected:\n{expected_conf}\n\nActual:\n{actual_conf}"
    )

def test_cron_schedule_file():
    cron_path = "/home/user/lb.cron"
    assert os.path.isfile(cron_path), f"Cron file {cron_path} does not exist."

    with open(cron_path, 'r') as f:
        content = f.read().strip()

    # Regex to match every 5 minutes schedule
    cron_pattern = r'^(\*/5|0-59/5)\s+\*\s+\*\s+\*\s+\*\s+/home/user/update_lb\.sh$'
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith('#')]

    assert len(lines) == 1, f"Expected exactly one active cron line in {cron_path}, found {len(lines)}."

    match = re.match(cron_pattern, lines[0])
    assert match, f"Cron line '{lines[0]}' does not match the expected pattern for running every 5 minutes."