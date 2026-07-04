# test_final_state.py
import os
import subprocess
import random
import yaml
import pytest

def test_yaml_patcher_installed():
    """Verify that yaml-patcher is installed and runnable."""
    bin_path = os.path.expanduser("~/.local/bin/yaml-patcher")
    assert os.path.isfile(bin_path), f"Expected yaml-patcher binary at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"yaml-patcher binary at {bin_path} is not executable"

    result = subprocess.run([bin_path, "--version"], capture_output=True, text=True)
    assert result.returncode == 0, f"yaml-patcher --version failed: {result.stderr}"
    assert "2.1.0" in result.stdout or "2.1.0" in result.stderr, "yaml-patcher version is not 2.1.0"

def test_systemd_service():
    """Verify systemd service and script."""
    script_path = "/home/user/watch.sh"
    assert os.path.isfile(script_path), f"Watch script {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Watch script {script_path} is not executable"

    service_path = "/home/user/.config/systemd/user/manifest-watcher.service"
    assert os.path.isfile(service_path), f"Systemd service file {service_path} does not exist"

    # We cannot reliably run systemctl --user in this environment without a full user session, 
    # but we can check if it's symlinked in the wants/requires directory.
    enabled_path = "/home/user/.config/systemd/user/default.target.wants/manifest-watcher.service"

    # Just check if systemctl can see it as enabled if possible, or fallback to symlink check
    try:
        res = subprocess.run(["systemctl", "--user", "is-enabled", "manifest-watcher.service"], capture_output=True, text=True)
        if res.returncode == 0 and "enabled" in res.stdout:
            return
    except Exception:
        pass

    assert os.path.islink(enabled_path) or os.path.isfile(enabled_path), "Service is not enabled (missing symlink in default.target.wants)"

def generate_random_deployment(seed):
    """Generate a random Kubernetes Deployment YAML."""
    random.seed(seed)

    name = f"app-{random.randint(1000, 9999)}"
    num_containers = random.randint(1, 5)

    containers = []
    for i in range(num_containers):
        container = {
            "name": f"container-{i}",
            "image": f"nginx:{random.choice(['latest', '1.19', '1.20'])}"
        }

        # Randomly include the audit-vault mount to test idempotency
        if random.random() > 0.5:
            container["volumeMounts"] = [
                {
                    "name": "audit-vault",
                    "mountPath": "/var/log/audit"
                }
            ]

        containers.append(container)

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": name
        },
        "spec": {
            "replicas": random.randint(1, 3),
            "template": {
                "metadata": {
                    "labels": {
                        "app": name
                    }
                },
                "spec": {
                    "containers": containers
                }
            }
        }
    }

    # Randomly include the audit-vault volume to test idempotency
    if random.random() > 0.5:
        deployment["spec"]["template"]["spec"]["volumes"] = [
            {
                "name": "audit-vault",
                "emptyDir": {}
            }
        ]

    return yaml.dump(deployment)

def test_manifest_processor_fuzz_equivalence():
    """Verify bit-exact equivalence of manifest-processor against the oracle."""
    agent_prog = "/home/user/manifest-processor"
    oracle_prog = "/opt/oracle/manifest-processor-oracle"

    assert os.path.isfile(agent_prog), f"Agent program {agent_prog} does not exist"
    assert os.access(agent_prog, os.X_OK), f"Agent program {agent_prog} is not executable"
    assert os.path.isfile(oracle_prog), f"Oracle program {oracle_prog} does not exist"

    N = 100 # Reduced from 500 for test speed, sufficient for fuzzing

    for i in range(N):
        input_yaml = generate_random_deployment(i)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_prog], 
            input=input_yaml, 
            capture_output=True, 
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}:\n{input_yaml}\nError: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_prog], 
            input=input_yaml, 
            capture_output=True, 
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent program failed on input {i}:\n{input_yaml}\nError: {agent_proc.stderr}"
        agent_out = agent_proc.stdout

        # Compare
        if agent_out != oracle_out:
            pytest.fail(
                f"Mismatch on input {i}!\n\n"
                f"INPUT:\n{input_yaml}\n\n"
                f"ORACLE OUTPUT:\n{oracle_out}\n\n"
                f"AGENT OUTPUT:\n{agent_out}"
            )