# test_final_state.py

import os
import time
import json
import subprocess
import pytest

def test_config_tracker_and_archive_size():
    """
    Starts the services, runs the agent's script, generates 50 unoptimized JSON files,
    waits for processing, and verifies the final archive size metric.
    """
    # 1. Start the background services
    start_script = '/app/start_services.sh'
    if os.path.exists(start_script):
        subprocess.run(['bash', start_script], check=True)
    time.sleep(2)  # Give services a moment to start

    # 2. Start the agent's script
    agent_process = None
    if os.path.exists('/home/user/run.sh'):
        agent_process = subprocess.Popen(['bash', '/home/user/run.sh'])
    elif os.path.exists('/home/user/config_tracker.py'):
        agent_process = subprocess.Popen(['python3', '/home/user/config_tracker.py'])
    else:
        pytest.fail("Neither /home/user/run.sh nor /home/user/config_tracker.py was found.")

    try:
        # 3. Generate 50 large, unoptimized JSON files
        mount_dir = '/home/user/config_mount'
        os.makedirs(mount_dir, exist_ok=True)

        for i in range(50):
            # Create a deeply nested dictionary with nulls and extensive whitespace
            data = {
                "config_id": i,
                "description": f"Configuration file number {i}",
                "settings": {
                    "enabled": True,
                    "timeout": 300,
                    "features": {
                        "beta": None,
                        "experimental": [None, "flag1", "flag2", None],
                        "legacy": None
                    }
                },
                "padding_for_size": " " * 500,  # simulate large unoptimized strings
                "empty_field": None
            }

            file_path = os.path.join(mount_dir, f'config_{i}.json')
            with open(file_path, 'w') as f:
                # Dump with indentation to create structural whitespace
                json.dump(data, f, indent=4)

            # Small sleep to ensure file system events trigger predictably
            time.sleep(0.1)

        # 4. Wait for the agent's script to finish processing
        # We wait a reasonable amount of time for 50 files to be processed and archived
        time.sleep(5)

        # 5. Check the archive size metric
        archive_path = '/home/user/archives/config_history.tar.gz'
        assert os.path.exists(archive_path), f"Archive file not found at {archive_path}. The script failed to create it."

        size = os.path.getsize(archive_path)

        # Metric Requirement: Archive size strictly < 15000 bytes
        assert size < 15000, (
            f"Metric failed: Archive size {size} >= 15000 bytes. "
            f"Ensure you are removing all whitespace, newlines, and null values, "
            f"and using maximum gzip compression."
        )

    finally:
        # Cleanup: stop the agent's script
        if agent_process:
            agent_process.terminate()
            try:
                agent_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                agent_process.kill()