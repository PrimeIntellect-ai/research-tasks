# test_final_state.py
import os
import stat
import math
import pytest

def get_inputs():
    raw_flows_path = "/home/user/raw_flows.log"
    pricing_path = "/home/user/pricing.csv"
    allowed_routes_path = "/home/user/allowed_routes.txt"

    flows = {}
    if os.path.isfile(raw_flows_path):
        with open(raw_flows_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    dst_ip = parts[2]
                    bytes_transferred = int(parts[3])
                    current_interface = parts[4]
                    if dst_ip not in flows:
                        flows[dst_ip] = {"bytes": 0, "interface": current_interface}
                    flows[dst_ip]["bytes"] += bytes_transferred

    pricing = {}
    if os.path.isfile(pricing_path):
        with open(pricing_path, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    pricing[parts[0]] = float(parts[1])

    allowed_routes = {}
    if os.path.isfile(allowed_routes_path):
        with open(allowed_routes_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    allowed_routes[parts[0]] = parts[1:]

    return flows, pricing, allowed_routes

def test_aggregated_flows():
    flows, _, _ = get_inputs()
    agg_path = "/home/user/aggregated_flows.txt"
    assert os.path.isfile(agg_path), f"Missing file: {agg_path}"

    with open(agg_path, "r") as f:
        lines = f.read().strip().split("\n")

    parsed_flows = {}
    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split()
        assert len(parts) == 3, f"Invalid format in aggregated_flows.txt: {line}"
        dst_ip, iface, total_bytes = parts[0], parts[1], int(parts[2])
        parsed_flows[dst_ip] = {"bytes": total_bytes, "interface": iface}

    assert parsed_flows == flows, f"Aggregated flows do not match expected: {parsed_flows} vs {flows}"

def test_savings_log():
    flows, pricing, allowed_routes = get_inputs()
    savings_path = "/home/user/savings.log"
    assert os.path.isfile(savings_path), f"Missing file: {savings_path}"

    total_savings = 0.0
    for dst_ip, data in flows.items():
        current_iface = data["interface"]
        total_bytes = data["bytes"]
        gb = total_bytes / 1073741824.0

        current_cost = gb * pricing.get(current_iface, 0.0)

        allowed = allowed_routes.get(dst_ip, [])
        cheapest_iface = min(allowed, key=lambda x: pricing.get(x, float('inf')))
        optimized_cost = gb * pricing.get(cheapest_iface, 0.0)

        total_savings += (current_cost - optimized_cost)

    expected_savings_str = f"Total Savings: ${total_savings:.2f}"

    with open(savings_path, "r") as f:
        content = f.read().strip()

    assert content == expected_savings_str, f"savings.log content '{content}' does not match expected '{expected_savings_str}'"

def test_update_routes_sh():
    flows, pricing, allowed_routes = get_inputs()
    script_path = "/home/user/update_routes.sh"
    assert os.path.isfile(script_path), f"Missing file: {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

    with open(script_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n") if line.strip()]

    assert lines[0] == "#!/bin/bash", f"update_routes.sh does not start with #!/bin/bash"

    expected_commands = set()
    for dst_ip, data in flows.items():
        allowed = allowed_routes.get(dst_ip, [])
        cheapest_iface = min(allowed, key=lambda x: pricing.get(x, float('inf')))
        expected_commands.add(f"ip route replace {dst_ip} dev {cheapest_iface}")

    actual_commands = set(lines[1:])
    assert actual_commands == expected_commands, f"update_routes.sh commands {actual_commands} do not match expected {expected_commands}"

def test_scripts_exist():
    assert os.path.isfile("/home/user/aggregate_flows.sh"), "Missing /home/user/aggregate_flows.sh"
    assert os.path.isfile("/home/user/cost_optimizer.c"), "Missing /home/user/cost_optimizer.c"
    assert os.path.isfile("/home/user/run_optimization.sh"), "Missing /home/user/run_optimization.sh"
    assert os.path.isfile("/home/user/cost_optimizer"), "Missing compiled binary /home/user/cost_optimizer"