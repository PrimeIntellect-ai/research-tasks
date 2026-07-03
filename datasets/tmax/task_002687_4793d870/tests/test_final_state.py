# test_final_state.py

import os
import subprocess
import random
import string
import tempfile
import pytest

def test_msmtp_installed():
    msmtp_bin = "/home/user/local/bin/msmtp"
    assert os.path.isfile(msmtp_bin), f"{msmtp_bin} does not exist. Was it installed correctly?"
    assert os.access(msmtp_bin, os.X_OK), f"{msmtp_bin} is not executable."

    result = subprocess.run([msmtp_bin, "--version"], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {msmtp_bin} --version failed."
    assert "1.8.24" in result.stdout, f"Expected version 1.8.24 in output, got: {result.stdout}"

def test_systemd_unit_file():
    unit_file = "/home/user/.config/systemd/user/msmtp-relay.service"
    assert os.path.isfile(unit_file), f"Systemd unit file {unit_file} is missing."

    with open(unit_file, "r") as f:
        content = f.read()

    assert "ExecStart=/home/user/local/bin/msmtpd" in content, \
        f"Unit file does not contain ExecStart=/home/user/local/bin/msmtpd. Content:\n{content}"

def generate_fuzz_email():
    headers = []

    # Decide if we include List-Id
    if random.random() < 0.5:
        list_id_val = random.choice(["dev.local", "announce.local", "other.local", "DEV.LOCAL", "AnNoUnCe.LoCaL"])
        header_name = random.choice(["List-Id", "list-id", "LIST-ID", "List-id"])
        headers.append(f"{header_name}: {list_id_val}")

    # Decide if we include Subject
    if random.random() < 0.5:
        subj_val = random.choice(["[URGENT] help", "normal email", "[urgent] stuff", "[URGENT]"])
        header_name = random.choice(["Subject", "subject", "SUBJECT"])
        headers.append(f"{header_name}: {subj_val}")

    # Add some random junk headers
    for _ in range(random.randint(1, 5)):
        name = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 10)))
        val = ''.join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(10, 50)))
        headers.append(f"{name}: {val}")

    random.shuffle(headers)
    body = ''.join(random.choices(string.ascii_letters + string.digits + " \n", k=random.randint(20, 100)))

    return "\n".join(headers) + "\n\n" + body

def test_fuzz_equivalence():
    agent_script = "/home/user/mail_router.sh"
    oracle_script = "/app/oracle_router.sh"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(500):
            email_content = generate_fuzz_email()
            input_file = os.path.join(tmpdir, f"email_{i}.txt")
            with open(input_file, "w") as f:
                f.write(email_content)

            agent_result = subprocess.run(["bash", agent_script, input_file], capture_output=True, text=True)
            oracle_result = subprocess.run(["bash", oracle_script, input_file], capture_output=True, text=True)

            assert agent_result.returncode == 0, f"Agent script failed on input {i}"
            assert oracle_result.returncode == 0, f"Oracle script failed on input {i}"

            agent_out = agent_result.stdout.strip()
            oracle_out = oracle_result.stdout.strip()

            assert agent_out == oracle_out, \
                f"Mismatch on fuzz input {i}!\nInput:\n{email_content}\n\nExpected: {oracle_out}\nGot: {agent_out}"