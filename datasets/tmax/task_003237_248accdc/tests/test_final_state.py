# test_final_state.py

import os
import json
import subprocess
import pytest

def test_metrics_out_json():
    out_file = "/home/user/metrics_out.json"
    assert os.path.isfile(out_file), f"{out_file} does not exist. Did you run the pipeline script?"

    with open(out_file, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {out_file} is not valid JSON: {content}")

    assert "avg_mem" in data, f"JSON output missing 'avg_mem' key: {data}"
    assert data["avg_mem"] == 1500, f"Expected avg_mem to be 1500, got {data['avg_mem']}"

def test_dashboard_conf_content():
    conf_file = "/home/user/dashboard.conf"
    assert os.path.isfile(conf_file), f"{conf_file} does not exist."

    with open(conf_file, "r") as f:
        content = f.read()

    assert "port=9090" in content, f"{conf_file} is missing 'port=9090'"
    assert "mode=production" in content, f"{conf_file} is missing 'mode=production'"

def test_dashboard_conf_acl():
    conf_file = "/home/user/dashboard.conf"
    assert os.path.isfile(conf_file), f"{conf_file} does not exist."

    result = subprocess.run(["getfacl", conf_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run getfacl on {conf_file}"

    acl_lines = result.stdout.splitlines()
    expected_acl = "user:nobody:r--"

    has_acl = any(line.startswith(expected_acl) for line in acl_lines)
    assert has_acl, f"ACL for 'nobody' is not set to read-only. getfacl output:\n{result.stdout}"

def test_tunnel_sh_content():
    tunnel_file = "/home/user/tunnel.sh"
    assert os.path.isfile(tunnel_file), f"{tunnel_file} does not exist."

    with open(tunnel_file, "r") as f:
        content = f.read()

    assert "-L" in content and "9090:localhost:8080" in content.replace(" ", ""), "tunnel.sh missing correct -L port forwarding configuration"
    assert "-i" in content and "/home/user/.ssh/dashboard_key" in content, "tunnel.sh missing correct -i identity file configuration"
    assert "backend-server" in content, "tunnel.sh missing 'backend-server'"
    assert "-f" in content.split(), "tunnel.sh missing '-f' flag to run in background"
    assert "-N" in content.split(), "tunnel.sh missing '-N' flag to not execute a remote command"

def test_pipeline_script_exists_and_executable():
    pipeline_file = "/home/user/run_pipeline.sh"
    assert os.path.isfile(pipeline_file), f"{pipeline_file} does not exist."
    assert os.access(pipeline_file, os.X_OK), f"{pipeline_file} is not executable."

def test_aggregator_compiled():
    aggregator_bin = "/home/user/aggregator"
    assert os.path.isfile(aggregator_bin), f"{aggregator_bin} does not exist. Did you compile the C++ program?"
    assert os.access(aggregator_bin, os.X_OK), f"{aggregator_bin} is not executable."

def test_fetch_exp_exists_and_executable():
    fetch_file = "/home/user/fetch.exp"
    assert os.path.isfile(fetch_file), f"{fetch_file} does not exist."
    # It might be run via `expect /home/user/fetch.exp`, so X_OK is not strictly required, 
    # but checking existence is good.