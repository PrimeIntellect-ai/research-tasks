# test_final_state.py

import os
import subprocess
import time
import glob
import pytest
import redis

def test_service_configuration():
    """
    Validates that the services.env file is correctly configured,
    and that starting the services results in a successful pipeline run.
    """
    env_file = "/home/user/services.env"
    assert os.path.exists(env_file), f"Environment file {env_file} is missing."

    # Parse the env file to pass to the subprocess
    env = os.environ.copy()
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if line.startswith('export '):
                    line = line[7:]
                if '=' in line:
                    key, val = line.split('=', 1)
                    env[key.strip()] = val.strip().strip('"\'')

    # Ensure required keys exist
    assert 'REDIS_HOST' in env, "REDIS_HOST not defined in services.env"
    assert 'REDIS_PORT' in env, "REDIS_PORT not defined in services.env"
    assert 'MESH_API_URL' in env, "MESH_API_URL not defined in services.env"

    # Run the start script with the sourced environment
    subprocess.run(["/bin/bash", "/app/start_services.sh"], env=env)

    # Wait for the pipeline to complete
    time.sleep(5)

    # Check Redis for the pipeline status
    try:
        r = redis.Redis(host=env.get('REDIS_HOST', '127.0.0.1'), port=int(env.get('REDIS_PORT', 6379)))
        status = r.get("pipeline_status")
        assert status is not None, "Redis key 'pipeline_status' not found. Pipeline may have failed."
        assert status.decode('utf-8') == "COMPLETED", f"Expected pipeline_status to be 'COMPLETED', got {status.decode('utf-8')}"
    except redis.exceptions.ConnectionError:
        pytest.fail("Failed to connect to Redis. Ensure REDIS_HOST and REDIS_PORT are correct and Redis is running.")
    finally:
        if 'r' in locals():
            r.close()

def test_adversarial_filter():
    """
    Validates the filter_sequences.py script against the adversarial corpus.
    """
    script_path = "/home/user/filter_sequences.py"
    assert os.path.exists(script_path), f"Script {script_path} is missing."

    clean_dir = "/app/test_data/clean/"
    evil_dir = "/app/test_data/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*.fasta"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.fasta"))

    assert clean_files, f"No clean files found in {clean_dir}."
    assert evil_files, f"No evil files found in {evil_dir}."

    clean_failures = []
    for f in clean_files:
        res = subprocess.run(["python3", script_path, f], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        res = subprocess.run(["python3", script_path, f], capture_output=True)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(f))

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    assert not errors, " | ".join(errors)