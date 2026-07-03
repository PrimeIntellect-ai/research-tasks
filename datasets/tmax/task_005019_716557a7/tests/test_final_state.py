# test_final_state.py
import os
import random
import string
import subprocess
import tarfile
import pytest

def test_fuzz_equivalence():
    """Test that new_router matches legacy_router on 10000 random inputs."""
    legacy_router = "/app/legacy_router"
    new_router_src = "/home/user/new_router.c"
    new_router = "/home/user/new_router"

    assert os.path.exists(legacy_router), f"Oracle missing at {legacy_router}"
    assert os.path.exists(new_router_src), f"Agent source missing at {new_router_src}"

    # Compile the agent's code if the binary doesn't exist or just to be sure
    compile_proc = subprocess.run(["gcc", new_router_src, "-o", new_router], capture_output=True)
    assert compile_proc.returncode == 0, f"Failed to compile {new_router_src}:\n{compile_proc.stderr.decode()}"

    assert os.path.exists(new_router), f"Agent binary missing at {new_router}"

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for _ in range(10000):
        length = random.randint(1, 64)
        fuzz_input = ''.join(random.choice(charset) for _ in range(length))

        oracle_proc = subprocess.run([legacy_router, fuzz_input], capture_output=True, text=True)
        agent_proc = subprocess.run([new_router, fuzz_input], capture_output=True, text=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {fuzz_input}"
        assert agent_proc.returncode == 0, f"Agent failed on input: {fuzz_input}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on input '{fuzz_input}': Expected '{oracle_out}', got '{agent_out}'"

def test_bashrc_env_var():
    """Verify ROUTER_MODE=migration is in .bashrc."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"Missing {bashrc_path}"
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert "ROUTER_MODE=migration" in content, "ROUTER_MODE=migration not found in .bashrc"

def test_proxy_conf():
    """Verify proxy.conf contains listen 9000 and the 4 backend ports."""
    conf_path = "/home/user/proxy.conf"
    assert os.path.exists(conf_path), f"Missing {conf_path}"
    with open(conf_path, "r") as f:
        content = f.read()

    assert "listen 9000" in content or "listen  9000" in content, "listen 9000 directive missing in proxy.conf"
    for port in [8080, 8081, 8082, 8083]:
        assert str(port) in content, f"Port {port} missing in proxy.conf"

def test_expect_script():
    """Verify verify_deployment.exp exists."""
    exp_path = "/home/user/verify_deployment.exp"
    assert os.path.exists(exp_path), f"Missing {exp_path}"

def test_backup_script():
    """Verify backup_strategy.sh works and creates the correct tarball."""
    script_path = "/home/user/backup_strategy.sh"
    tar_path = "/home/user/backups/deploy_backup.tar.gz"

    assert os.path.exists(script_path), f"Missing {script_path}"

    # Run the backup script
    proc = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert proc.returncode == 0, f"Backup script failed:\n{proc.stderr}"

    assert os.path.exists(tar_path), f"Backup tarball not created at {tar_path}"

    # Check tarball contents
    with tarfile.open(tar_path, "r:gz") as tar:
        names = [os.path.basename(m.name) for m in tar.getmembers()]
        assert "proxy.conf" in names, "proxy.conf missing from backup tarball"
        assert "new_router.c" in names, "new_router.c missing from backup tarball"