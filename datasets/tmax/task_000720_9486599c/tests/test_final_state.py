# test_final_state.py
import os
import subprocess
import pytest
import yaml

def test_docker_compose_configuration():
    path = "/home/user/edge-stack/docker-compose.yml"
    assert os.path.isfile(path), f"Docker Compose file is missing at {path}"

    with open(path, 'r') as f:
        compose_data = yaml.safe_load(f)

    # Check that both services exist
    assert "services" in compose_data
    assert "api" in compose_data["services"]
    assert "worker" in compose_data["services"]

    # Check that both use edge_net
    api_networks = compose_data["services"]["api"].get("networks", [])
    worker_networks = compose_data["services"]["worker"].get("networks", [])

    assert "edge_net" in api_networks, "api service is not connected to edge_net"
    assert "edge_net" in worker_networks, "worker service is not connected to edge_net"

    # Check that edge_net is defined in top-level networks
    assert "networks" in compose_data
    assert "edge_net" in compose_data["networks"], "edge_net is not defined in the top-level networks block"

def test_docker_containers_running_and_connected():
    # Check if containers are running
    cmd_ps = ["docker", "ps", "--format", "{{.Names}}"]
    result_ps = subprocess.run(cmd_ps, capture_output=True, text=True)

    assert result_ps.returncode == 0, "Failed to run docker ps"
    running_containers = result_ps.stdout.splitlines()

    api_container = next((c for c in running_containers if "api" in c), None)
    worker_container = next((c for c in running_containers if "worker" in c), None)

    assert api_container is not None, "api container is not running"
    assert worker_container is not None, "worker container is not running"

    # Test connectivity from worker to api using curl
    cmd_curl = ["docker", "exec", worker_container, "curl", "-s", "http://api"]
    result_curl = subprocess.run(cmd_curl, capture_output=True, text=True)

    assert result_curl.returncode == 0, f"Worker could not reach API. Curl output: {result_curl.stderr}"
    assert "Welcome to nginx!" in result_curl.stdout or "<html" in result_curl.stdout, "API did not return expected Nginx response"

def test_sanitizer_script_adversarial_corpus():
    script_path = "/home/user/sanitize.py"
    assert os.path.isfile(script_path), f"Sanitizer script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Sanitizer script at {script_path} is not executable"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus missing at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.txt')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.txt')]

    failed_clean = []
    for f in clean_files:
        res = subprocess.run([script_path, f], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        res = subprocess.run([script_path, f], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(f))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))