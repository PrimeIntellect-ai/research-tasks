# test_final_state.py

import os
import stat
import random
import string
import subprocess
import pytest

CLIENT_SCRIPT = "/home/user/client.sh"
ORACLE_SCRIPT = "/tmp/oracle.sh"

@pytest.fixture(scope="session", autouse=True)
def setup_oracle():
    oracle_content = '#!/bin/bash\necho "${1^^}_ACK"\n'
    with open(ORACLE_SCRIPT, "w") as f:
        f.write(oracle_content)
    st = os.stat(ORACLE_SCRIPT)
    os.chmod(ORACLE_SCRIPT, st.st_mode | stat.S_IEXEC)

def test_client_script_exists_and_executable():
    assert os.path.exists(CLIENT_SCRIPT), f"Agent script {CLIENT_SCRIPT} does not exist."
    assert os.path.isfile(CLIENT_SCRIPT), f"{CLIENT_SCRIPT} is not a file."
    assert os.access(CLIENT_SCRIPT, os.X_OK), f"{CLIENT_SCRIPT} is not executable."

def test_fuzz_equivalence():
    random.seed(42)

    for i in range(50):
        length = random.randint(5, 32)
        fuzz_input = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_SCRIPT, fuzz_input],
            capture_output=True,
            text=True,
            check=True
        )
        expected_output = oracle_proc.stdout.strip()

        # Run agent's script
        try:
            agent_proc = subprocess.run(
                ["/bin/bash", CLIENT_SCRIPT, fuzz_input],
                capture_output=True,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input '{fuzz_input}'. "
                        "This likely means the Docker Compose network is still misconfigured "
                        "and the request is hanging.")

        agent_output = agent_proc.stdout.strip()

        assert agent_proc.returncode == 0, (
            f"Agent script failed with return code {agent_proc.returncode} on input '{fuzz_input}'.\n"
            f"Stderr: {agent_proc.stderr}"
        )

        assert agent_output == expected_output, (
            f"Output mismatch on input '{fuzz_input}'.\n"
            f"Expected (Oracle): {expected_output}\n"
            f"Actual (Agent): {agent_output}"
        )