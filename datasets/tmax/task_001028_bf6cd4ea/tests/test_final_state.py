# test_final_state.py

import os
import subprocess
import random
import string
import json
import pytest

def test_proxy_package_fixed_and_installed():
    """Test that the cloud-proxy package is installed in editable mode and the POST perturbation is removed."""
    # Check if installed
    result = subprocess.run(["pip", "list", "--format=json"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run pip list"
    packages = json.loads(result.stdout)
    installed = any(pkg.get("name") == "cloud-proxy" for pkg in packages)
    assert installed, "cloud-proxy package is not installed."

    # Check that perturbation is removed
    server_file = "/app/cloud-proxy-0.1.0/cloud_proxy/server.py"
    assert os.path.isfile(server_file), f"{server_file} is missing."
    with open(server_file, "r") as f:
        content = f.read()

    # The perturbation was: if request.method == "POST": return web.Response(status=403, text="POST forbidden")
    assert 'status=403' not in content or 'POST forbidden' not in content, "The POST perturbation is still present in server.py."

def test_fstab_configuration():
    """Test that the fstab configuration file is correct."""
    fstab_path = "/home/user/migration_fstab.txt"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    # It should contain a single valid fstab entry
    # Format: <file system> <dir> <type> <options> <dump> <pass>
    parts = content.split()
    assert len(parts) >= 4, f"fstab entry seems incomplete: {content}"
    assert parts[0] == "10.0.0.5:/var/nfs/legacy", f"Incorrect file system: {parts[0]}"
    assert parts[1] == "/mnt/legacy_assets", f"Incorrect mount point: {parts[1]}"
    assert parts[2] == "nfs4", f"Incorrect file system type: {parts[2]}"

    options = parts[3].split(",")
    expected_options = ["ro", "nosuid", "nodev", "noexec", "bg", "soft", "rsize=8192", "wsize=8192"]
    for opt in expected_options:
        assert opt in options, f"Missing option '{opt}' in fstab entry."

def test_docker_compose_configuration():
    """Test that the docker-compose.yml file is configured correctly."""
    compose_path = "/home/user/docker-compose.yml"
    assert os.path.isfile(compose_path), f"File {compose_path} does not exist."

    with open(compose_path, "r") as f:
        content = f.read()

    assert "cloud-proxy:" in content or "cloud-proxy" in content, "Service 'cloud-proxy' not defined in docker-compose.yml"
    assert "python:3.9-slim" in content, "Image 'python:3.9-slim' not specified in docker-compose.yml"
    assert "8080" in content, "Port 8080 not exposed in docker-compose.yml"
    assert "/home/user/migrator_router.py:/usr/local/bin/router.py" in content.replace(" ", ""), "Volume mount for router.py is incorrect or missing."

def test_routing_logic_fuzz_equivalence():
    """Test that the routing logic matches the oracle on random fuzzed inputs."""
    agent_script = "/home/user/migrator_router.py"
    oracle_script = "/opt/oracle/migrator_router.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} does not exist."

    random.seed(42)
    charset = string.ascii_letters + string.digits + "/.?=&_-"
    seeds = ["/static/", ".php", "/api/v1/", "/api/v2/"]

    # Generate 500 inputs to avoid test timeout while still providing good coverage
    N = 500
    inputs = []
    for _ in range(N):
        length = random.randint(5, 150)
        base = "".join(random.choices(charset, k=length))
        # Inject seeds randomly
        if random.random() < 0.5:
            seed = random.choice(seeds)
            pos = random.randint(0, len(base))
            base = base[:pos] + seed + base[pos:]
        inputs.append(base)

    for uri in inputs:
        oracle_res = subprocess.run(["python3", oracle_script, uri], capture_output=True, text=True)
        agent_res = subprocess.run(["python3", agent_script, uri], capture_output=True, text=True)

        assert agent_res.returncode == 0, f"Agent script failed on input: {uri}\nError: {agent_res.stderr}"
        assert oracle_res.stdout.strip() == agent_res.stdout.strip(), (
            f"Mismatch on input: {uri}\n"
            f"Expected (Oracle): {oracle_res.stdout.strip()}\n"
            f"Got (Agent):       {agent_res.stdout.strip()}"
        )