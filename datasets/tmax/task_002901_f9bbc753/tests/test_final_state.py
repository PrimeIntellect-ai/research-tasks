# test_final_state.py

import os
import re
import random
import string
import subprocess
import pytest

def test_nginx_configuration():
    """Check that nginx.conf is properly configured."""
    conf_path = '/app/nginx.conf'
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "8080" in content, "Nginx is not configured to listen on port 8080."
    assert "/app/docs" in content, "Nginx is not configured to serve /app/docs/."
    assert "disable_symlinks off;" in content, "Nginx is not configured with 'disable_symlinks off;'."

def test_watcher_configuration():
    """Check that watcher.conf points to the correct script."""
    conf_path = '/app/watcher.conf'
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "PROCESS_SCRIPT=/home/user/parse_docs.sh" in content, "watcher.conf does not point to /home/user/parse_docs.sh."

def test_script_exists_and_executable():
    """Check that the parsing script exists and is executable."""
    script_path = '/home/user/parse_docs.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def generate_random_record():
    path_len = random.randint(5, 20)
    path = "/tmp/" + "".join(random.choices(string.ascii_lowercase, k=path_len)) + ".md"

    author_len = random.randint(5, 15)
    author = "".join(random.choices(string.ascii_letters + " ", k=author_len)).strip()
    if not author:
        author = "Default Author"

    num_tags = random.randint(1, 10)
    tags = []
    for _ in range(num_tags):
        tags.append("".join(random.choices(string.ascii_lowercase, k=random.randint(3, 8))))

    ws1 = " " * random.randint(0, 3)
    ws2 = " " * random.randint(0, 3)
    ws3 = " " * random.randint(0, 3)

    tags_str = ("," + " " * random.randint(0, 2)).join(tags)

    return f"PATH:{ws1}{path}\nAUTHOR:{ws2}{author}\nTAGS:{ws3}{tags_str}"

def test_fuzz_equivalence():
    """Fuzz test the parsing script against the oracle for exact stdout equivalence."""
    oracle_path = '/app/oracle.py'
    agent_script = '/home/user/parse_docs.sh'

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} missing."

    random.seed(42)

    for i in range(100):
        num_records = random.randint(1, 50)
        records = [generate_random_record() for _ in range(num_records)]

        # Randomly add extra blank lines to test robustness
        sep = "\n" + "\n" * random.randint(1, 2)
        fuzz_input = sep.join(records) + "\n"

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=fuzz_input,
                text=True,
                capture_output=True,
                check=True
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input:\n{fuzz_input}\nError: {e.stderr}")

        # Run agent script
        try:
            agent_proc = subprocess.run(
                [agent_script],
                input=fuzz_input,
                text=True,
                capture_output=True,
                check=True
            )
            agent_out = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input:\n{fuzz_input}\nError: {e.stderr}")

        assert agent_out == oracle_out, (
            f"Output mismatch on fuzz iteration {i}.\n"
            f"Input:\n{fuzz_input}\n"
            f"Expected (Oracle):\n{oracle_out}\n"
            f"Got (Agent):\n{agent_out}"
        )