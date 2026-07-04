# test_final_state.py

import os
import socket
import subprocess
import random
import pytest

def test_stage1_echo_server_running_and_fixed():
    """Test that the echo server is running and bound to the correct socket."""
    sock_path = "/tmp/upstream.sock"
    assert os.path.exists(sock_path), f"Socket file {sock_path} does not exist. Did you start the server?"

    # Test that it's a socket
    import stat
    mode = os.stat(sock_path).st_mode
    assert stat.S_ISSOCK(mode), f"{sock_path} is not a socket."

    # Test the echo functionality
    test_message = b"ping_test_123"
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(2.0)
        client.connect(sock_path)
        client.sendall(test_message)
        data = client.recv(1024)
        client.close()
    except Exception as e:
        pytest.fail(f"Failed to connect and communicate with the echo server at {sock_path}: {e}")

    assert data == test_message, f"Echo server did not return the expected message. Got {data}, expected {test_message}."

def test_stage2_fw_compiler_fuzz_equivalence():
    """Fuzz test the firewall compiler script against the oracle."""
    agent_script = "/home/user/fw_compiler.sh"
    oracle_script = "/opt/oracle/fw_oracle.sh"

    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable."

    random.seed(42)

    def random_ip(prefix):
        if prefix == "any": return "any"
        return prefix.replace("X", str(random.randint(1, 254)))

    src_prefixes = ["any", "192.168.1.X", "10.0.0.X"]
    dst_prefixes = ["any", "172.16.0.X", "10.1.1.X"]
    ports_list = ["any", "80", "443", "80,443", "22,23,24"]
    protos_list = ["tcp", "udp", "icmp"]
    actions_list = ["ACCEPT", "DROP", "REJECT"]

    for _ in range(1000):
        src = random_ip(random.choice(src_prefixes))
        dst = random_ip(random.choice(dst_prefixes))
        ports = random.choice(ports_list)
        proto = random.choice(protos_list)
        action = random.choice(actions_list)

        rule = f"{src};{dst};{ports};{proto};{action}"

        agent_res = subprocess.run([agent_script, rule], capture_output=True, text=True)
        oracle_res = subprocess.run([oracle_script, rule], capture_output=True, text=True)

        assert agent_res.returncode == 0, f"Agent script failed on input: {rule}\nStderr: {agent_res.stderr}"

        agent_out = agent_res.stdout.strip()
        oracle_out = oracle_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on input: {rule}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent):       {agent_out}"
        )

def test_stage3_cron_job_exists():
    """Test that the cron job is correctly configured."""
    try:
        crontab_out = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. No crontab for current user?")

    # Look for a cron job that runs every minute and checks for the socket
    # We'll check for the presence of the required logic elements rather than exact string matching
    # since there are multiple ways to write the bash command.

    found_valid_cron = False
    for line in crontab_out.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Check schedule: * * * * *
        parts = line.split(maxsplit=5)
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            cmd = parts[5]

            if schedule == "* * * * *":
                # Check for required elements in the command
                if "/tmp/upstream.sock" in cmd and "/home/user/monitor.log" in cmd and "DOWN" in cmd:
                    found_valid_cron = True
                    break

    assert found_valid_cron, "Could not find a valid cron job running every minute that checks /tmp/upstream.sock and logs DOWN to /home/user/monitor.log"