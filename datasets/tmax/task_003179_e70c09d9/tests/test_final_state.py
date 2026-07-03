# test_final_state.py

import os
import stat
import subprocess
import random
import string
import pytest

def test_monitor_key_permissions():
    """Check if the monitor key has 0600 permissions."""
    path = '/home/user/.ssh/monitor_key'
    assert os.path.isfile(path), f"{path} does not exist"
    st = os.stat(path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"{path} should have 0600 permissions, but has {oct(permissions)}"

def test_cron_job_exists():
    """Check that the cron job for monitor_sync.sh is set up."""
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Ensure crontab is set up."
    assert '/home/user/monitor_sync.sh' in result.stdout, "Cron job for monitor_sync.sh is missing from crontab."

def generate_fuzz_input():
    """Generate a random log file input matching the distribution."""
    num_lines = random.randint(0, 1000)
    lines = []
    services = [''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 20))) for _ in range(10)]

    last_ts = {s: random.randint(1600000000, 1700000000) for s in services}
    for _ in range(num_lines):
        if random.random() < 0.10:
            lines.append(''.join(random.choices(string.printable, k=random.randint(10, 50))))
            continue

        svc = random.choice(services)
        if random.random() < 0.10:
            # Chronological violation
            ts = last_ts[svc] - random.randint(1, 10000)
        else:
            # Valid chronological progression
            ts = last_ts[svc] + random.randint(0, 10000)
            last_ts[svc] = ts

        event = "HEARTBEAT_OK" if random.random() < 0.5 else "HEARTBEAT_FAIL"
        lines.append(f"[{ts}] {svc} {event}")

    return "\n".join(lines) + ("\n" if lines else "")

def test_fuzz_equivalence():
    """Fuzz test the agent's parser against the oracle parser."""
    oracle = '/app/oracle_parser'
    agent = '/home/user/log_parser.py'

    assert os.path.isfile(oracle), f"Oracle {oracle} missing."
    assert os.path.isfile(agent), f"Agent script {agent} missing."

    random.seed(42)
    # Run 100 iterations to balance thoroughness and test duration
    for i in range(100):
        fuzz_in = generate_fuzz_input()

        oracle_proc = subprocess.run([oracle], input=fuzz_in, text=True, capture_output=True)
        agent_proc = subprocess.run(['python3', agent], input=fuzz_in, text=True, capture_output=True)

        assert agent_proc.returncode == 0, f"Agent script crashed on fuzz input {i}:\n{agent_proc.stderr}"

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Output mismatch on fuzz iteration {i}.\n\n"
                f"--- Input (first 500 chars) ---\n{fuzz_in[:500]}...\n\n"
                f"--- Oracle Output ---\n{oracle_proc.stdout}\n"
                f"--- Agent Output ---\n{agent_proc.stdout}\n"
            )