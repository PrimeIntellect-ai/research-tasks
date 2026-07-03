# test_final_state.py

import os
import subprocess
import random
import string
import time
import urllib.request
import pytest

def generate_random_string(length):
    chars = string.ascii_letters + string.digits + string.punctuation + " \t\n" + "áéíóúñü"
    return ''.join(random.choice(chars) for _ in range(length)).encode('utf-8')

def test_cleaner_fuzz_equivalence():
    agent_path = "/app/cleaner"
    oracle_path = "/opt/oracle/oracle_cleaner"

    assert os.path.isfile(agent_path), f"Agent executable {agent_path} not found."
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable."

    random.seed(42)

    # Run a smaller number of fuzz iterations to keep the test fast
    for i in range(100):
        length = random.randint(0, 5000)
        input_data = generate_random_string(length)

        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)
        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on iteration {i}"
        assert agent_proc.stdout == oracle_proc.stdout, f"Output mismatch on iteration {i}. Input: {input_data!r}\nOracle: {oracle_proc.stdout!r}\nAgent: {agent_proc.stdout!r}"

def test_end_to_end_pipeline():
    start_script = "/app/start_all.sh"
    assert os.path.isfile(start_script), f"{start_script} not found."
    assert os.access(start_script, os.X_OK), f"{start_script} is not executable."

    # Start the pipeline
    proc = subprocess.Popen([start_script], shell=True, preexec_fn=os.setsid)
    time.sleep(5)

    try:
        # Send POST request
        req = urllib.request.Request("http://localhost:8080/ingest", data=b"Sample text!!", method="POST")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200

        # Poll Redis for the result
        result = None
        for _ in range(10):
            time.sleep(1)
            redis_proc = subprocess.run(["redis-cli", "LPOP", "clean_data"], capture_output=True, text=True)
            out = redis_proc.stdout.strip()
            if out and out != "(nil)":
                result = out
                break

        expected = "sample text_\nSTATS: 3"
        # The redis-cli might format newlines as literal \n or actual newlines depending on how it's called
        # We will normalize it to actual newlines for comparison if needed
        if result:
            result = result.replace('\\n', '\n').strip('"')

        assert result == expected, f"Expected {expected!r}, got {result!r}"
    finally:
        # Clean up the processes
        os.system("pkill -f 'python3 /app/api.py'")
        os.system("pkill -f 'nginx'")
        os.system("pkill -f 'worker.sh'")
        os.system("pkill -f 'redis-server'")