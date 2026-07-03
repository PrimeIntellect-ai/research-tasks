# test_final_state.py

import os
import stat
import subprocess
import random
import string
import pytest

def test_script_exists_and_executable():
    """Check that the script exists and is executable."""
    script_path = "/home/user/process_stream.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_cron_job_exists():
    """Verify the cron job is scheduled correctly."""
    try:
        result = subprocess.run(
            ["crontab", "-l", "-u", "user"],
            capture_output=True,
            text=True,
            check=True
        )
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab for user 'user'.")

    expected_cron = "30 2 * * * /home/user/process_stream.sh < /data/daily.csv > /data/processed.csv"

    # Check if the expected cron job is in the crontab
    found = False
    for line in crontab_content.splitlines():
        if line.strip() == expected_cron:
            found = True
            break

    assert found, f"Expected cron job not found in crontab. Expected: '{expected_cron}'"

def generate_random_csv_stream():
    """Generate a random CSV stream according to the fuzz distribution."""
    num_lines = random.randint(100, 500)
    lines = []
    for _ in range(num_lines):
        # id: random integer 1-100
        id_val = random.randint(1, 100)

        # category: random [A-Z]{4}
        category = "".join(random.choices(string.ascii_uppercase, k=4))

        # value: random float or empty string
        if random.random() < 0.2:
            value = ""
        else:
            value = f"{random.uniform(0.0, 1000.0):.2f}"

        # notes: random ISO-8859-1 bytes (0x20-0xFF, excluding 0x2C and 0x0A)
        note_length = random.randint(5, 50)
        valid_bytes = [b for b in range(0x20, 0x100) if b not in (0x2C, 0x0A)]
        notes_bytes = bytes(random.choices(valid_bytes, k=note_length))

        # Assemble line
        line = f"{id_val},{category},{value},".encode('iso-8859-1') + notes_bytes + b"\n"
        lines.append(line)

    return b"".join(lines)

def test_fuzz_equivalence():
    """Fuzz test to ensure the agent script perfectly replicates the oracle binary."""
    oracle_path = "/app/legacy_etl"
    agent_script = "/home/user/process_stream.sh"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}."

    random.seed(42)
    N = 200

    for i in range(N):
        input_data = generate_random_csv_stream()

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"
        oracle_out = oracle_proc.stdout

        # Run agent script
        agent_proc = subprocess.run(
            ["/bin/bash", agent_script],
            input=input_data,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed (exit code {agent_proc.returncode}) on input {i}:\n{agent_proc.stderr.decode('utf-8', errors='replace')}")

        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on random input {i}.\n"
                f"Input data length: {len(input_data)} bytes\n"
                f"Oracle output length: {len(oracle_out)} bytes\n"
                f"Agent output length: {len(agent_out)} bytes\n"
                f"First 200 bytes of oracle output: {oracle_out[:200]!r}\n"
                f"First 200 bytes of agent output: {agent_out[:200]!r}"
            )