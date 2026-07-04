# test_final_state.py

import os
import sys
import ipaddress
import subprocess
import pytest

def test_routes_conf_metric():
    raw_routes_path = "/home/user/raw_routes.txt"
    conf_path = "/home/user/deployed_router/routes.conf"

    assert os.path.isfile(raw_routes_path), f"Raw routes file {raw_routes_path} is missing."
    assert os.path.isfile(conf_path), f"Compiled routes file {conf_path} is missing."

    # Calculate truth metric
    with open(raw_routes_path, "r") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    networks = [ipaddress.IPv4Network(cidr, strict=False) for cidr in raw_lines]
    collapsed = list(ipaddress.collapse_addresses(networks))
    optimal_count = len(collapsed)

    # Read agent's output
    with open(conf_path, "r") as f:
        agent_lines = [line.strip() for line in f if line.strip()]

    agent_count = len(agent_lines)

    # Metric threshold check
    assert agent_count <= optimal_count, (
        f"Metric threshold failed: Agent produced {agent_count} routes, "
        f"but optimal aggregation is {optimal_count} routes."
    )

    # Optionally check if the agent's routes actually cover the same space
    agent_networks = [ipaddress.IPv4Network(cidr, strict=False) for cidr in agent_lines]
    agent_collapsed = list(ipaddress.collapse_addresses(agent_networks))
    assert set(agent_collapsed) == set(collapsed), "Agent's aggregated routes do not cover the exact same IP space as the raw routes."

def test_daemon_running():
    pid_file = "/home/user/daemon.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"
    pid = int(pid_str)

    # Check if process is running
    assert os.path.isdir(f"/proc/{pid}"), f"Process with PID {pid} is not running."

    with open(f"/proc/{pid}/cmdline", "rb") as f:
        cmdline = f.read().replace(b"\x00", b" ").decode("utf-8")

    assert "router_daemon" in cmdline, f"Process {pid} is not the router_daemon. Cmdline: {cmdline}"

def test_daemon_network_namespace():
    pid_file = "/home/user/daemon.pid"
    with open(pid_file, "r") as f:
        pid = f.read().strip()

    # Check if dummy0 exists in the namespace
    try:
        out = subprocess.check_output(["nsenter", "-t", pid, "-n", "ip", "addr", "show", "dummy0"], stderr=subprocess.STDOUT)
        out_str = out.decode("utf-8")
        assert "10.99.0.1/24" in out_str, f"dummy0 interface does not have the expected IP 10.99.0.1/24 in the daemon's namespace."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to inspect dummy0 in daemon's network namespace: {e.output.decode('utf-8')}")

    # Check if route exists in the namespace
    try:
        out = subprocess.check_output(["nsenter", "-t", pid, "-n", "ip", "route", "show"], stderr=subprocess.STDOUT)
        out_str = out.decode("utf-8")
        assert "192.168.100.0/24" in out_str, "Route to 192.168.100.0/24 is missing in the daemon's namespace."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to inspect routes in daemon's network namespace: {e.output.decode('utf-8')}")