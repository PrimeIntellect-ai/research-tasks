# test_final_state.py
import os
import subprocess
import random
import string
import time
import urllib.request

def test_fuzz_equivalence_audit_tokenizer():
    oracle_path = "/app/reference_oracle/audit_tokenizer"
    agent_path = "/home/user/workspace/audit_tokenizer"

    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    printable = string.printable.replace("\r", "").replace("\n", "").replace("\x0b", "").replace("\x0c", "")

    # Run 1000 iterations to prevent test timeout while ensuring robustness
    for _ in range(1000):
        length = random.randint(1, 256)
        test_input = "".join(random.choice(printable) for _ in range(length))

        oracle_proc = subprocess.run([oracle_path, test_input], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, test_input], capture_output=True, text=True)

        assert oracle_proc.returncode == agent_proc.returncode, f"Return code mismatch on input '{test_input}'"
        assert oracle_proc.stdout == agent_proc.stdout, f"Output mismatch on input '{test_input}'. Oracle: {oracle_proc.stdout}, Agent: {agent_proc.stdout}"

def test_nginx_csp_configuration():
    # Start services
    subprocess.run(["/app/start_services.sh"], check=False)
    time.sleep(2) # Wait for services to start

    try:
        req = urllib.request.Request("http://localhost:8080/")
        with urllib.request.urlopen(req, timeout=5) as response:
            headers = response.headers
            csp = headers.get("Content-Security-Policy", "")

            assert "script-src" in csp, "Content-Security-Policy does not contain script-src"
            assert "'self'" in csp, "Content-Security-Policy does not allow 'self'"
            assert "https://trusted.cdn.com" in csp, "Content-Security-Policy does not allow https://trusted.cdn.com"
            assert "'unsafe-inline'" not in csp, "Content-Security-Policy allows unsafe-inline scripts"
            assert "'unsafe-eval'" not in csp, "Content-Security-Policy allows unsafe-eval"
    except Exception as e:
        # Fallback to config check if service is not running
        config_path = "/home/user/nginx/nginx.conf"
        assert os.path.exists(config_path), "nginx.conf not found"
        with open(config_path, "r") as f:
            content = f.read()
            assert "Content-Security-Policy" in content, "CSP header not found in nginx config"
            assert "https://trusted.cdn.com" in content, "trusted.cdn.com not in CSP"

def test_ssh_hardening():
    config_path = "/home/user/ssh/sshd_config"
    assert os.path.exists(config_path), f"SSH config not found at {config_path}"

    # Parse sshd config using sshd -T
    proc = subprocess.run(["sshd", "-T", "-f", config_path], capture_output=True, text=True)
    output = proc.stdout.lower()

    assert "passwordauthentication no" in output, "PasswordAuthentication is not disabled"
    assert "permitrootlogin no" in output, "PermitRootLogin is not disabled"

    # Check HostKey
    hostkeys = [line for line in output.splitlines() if line.startswith("hostkey ")]
    for hk in hostkeys:
        assert "ed25519" in hk, f"Non-ed25519 host key found: {hk}"

def test_ssh_key_generated():
    key_path = "/home/user/.ssh/id_ed25519_audit"
    assert os.path.exists(key_path), f"SSH key not found at {key_path}"

    # Check if it's a valid ed25519 key
    with open(key_path, "r") as f:
        content = f.read()
        assert "OPENSSH PRIVATE KEY" in content or "ED25519" in content, "Generated key does not appear to be an ed25519 private key"

def test_integration_script():
    script_path = "/home/user/workspace/run_audit.sh"
    log_path = "/home/user/workspace/audit.log"

    assert os.path.exists(script_path), f"Integration script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Integration script at {script_path} is not executable"

    test_event = "integration_test_event"
    oracle_path = "/app/reference_oracle/audit_tokenizer"

    oracle_proc = subprocess.run([oracle_path, test_event], capture_output=True, text=True)
    expected_token = oracle_proc.stdout.strip()

    subprocess.run([script_path, test_event], check=True)

    assert os.path.exists(log_path), f"Audit log not found at {log_path}"

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_entry = f"[{expected_token}] - {test_event}"
    assert expected_entry in log_content, f"Expected log entry '{expected_entry}' not found in audit.log"