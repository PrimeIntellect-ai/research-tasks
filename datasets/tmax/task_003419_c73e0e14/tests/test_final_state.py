# test_final_state.py

import os
import subprocess
import random
import string
import tempfile
import pytest

def test_locale_installed():
    """Ensure the fr_FR.UTF-8 locale is installed and available."""
    result = subprocess.run(["locale", "-a"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run locale -a"
    locales = result.stdout.lower()
    assert "fr_fr.utf8" in locales or "fr_fr.utf-8" in locales, "Locale fr_FR.UTF-8 is not installed or generated."

def test_logrotate_config():
    """Check the logrotate configuration for daily rotation and 7 days retention."""
    conf_path = "/home/user/logrotate.conf"
    assert os.path.exists(conf_path), f"Logrotate config missing at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    # Check for keywords
    assert "daily" in content, "logrotate.conf is missing 'daily' directive."
    assert "rotate 7" in content, "logrotate.conf is missing 'rotate 7' directive."
    assert "/home/user/logs/" in content or "/home/user/logs/*" in content, "logrotate.conf does not target /home/user/logs/"

def test_wrapper_script_exists():
    """Ensure the wrapper script exists and is executable."""
    script_path = "/home/user/process_logs.sh"
    assert os.path.exists(script_path), f"Wrapper script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Wrapper script {script_path} is not executable"

def generate_log_lines(n):
    random.seed(42)
    lines = []
    for _ in range(n):
        length = random.randint(50, 500)
        base = "".join(random.choices(string.ascii_letters + string.digits + " :-", k=length))

        # Inject specific patterns
        if random.random() < 0.4:
            base += " Disconnecting: Too many authentication failures "
        elif random.random() < 0.4:
            base += " Disconnecting: Too many failures "

        if random.random() < 0.5:
            base += " fr_FR.UTF-8 "
        else:
            base += " en_US.UTF-8 "

        lines.append(base)
    return lines

def test_fuzz_equivalence():
    """Fuzz both the oracle and the agent's wrapper script and assert identical outputs."""
    oracle_path = "/opt/oracle/log-router-oracle"
    agent_script = "/home/user/process_logs.sh"

    assert os.path.exists(oracle_path), f"Oracle program missing at {oracle_path}"

    num_lines = 1000
    lines = generate_log_lines(num_lines)

    # Group lines into chunks to minimize subprocess overhead while still testing multi-line files
    chunk_size = 100
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    for i, chunk in enumerate(chunks):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("\n".join(chunk) + "\n")
            tmp_path = tmp.name

        try:
            oracle_res = subprocess.run([oracle_path, tmp_path], capture_output=True, text=True)
            agent_res = subprocess.run([agent_script, tmp_path], capture_output=True, text=True)

            assert agent_res.returncode == oracle_res.returncode, (
                f"Return code mismatch on chunk {i}.\n"
                f"Oracle exited with {oracle_res.returncode}, Agent exited with {agent_res.returncode}.\n"
                f"Agent stderr: {agent_res.stderr}"
            )

            assert agent_res.stdout == oracle_res.stdout, (
                f"Output mismatch on chunk {i}.\n"
                f"--- Oracle Output ---\n{oracle_res.stdout}\n"
                f"--- Agent Output ---\n{agent_res.stdout}\n"
            )
        finally:
            os.remove(tmp_path)