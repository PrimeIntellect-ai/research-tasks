# test_final_state.py
import os
import subprocess
import time
import hashlib
import pytest

def test_rescue_script_metric():
    script_path = '/home/user/rescue.sh'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # 1. Setup directories
    os.makedirs('/home/user/workspace', exist_ok=True)
    os.makedirs('/home/user/rescued_data', exist_ok=True)

    # 2. Run the agent's script in the background
    agent_proc = subprocess.Popen(
        ['nohup', script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )

    try:
        # 3. Give it a second to initialize
        time.sleep(1)

        # 4. Run the processor
        processor_path = '/app/proprietary_processor'
        assert os.path.exists(processor_path), f"Processor binary missing at {processor_path}."
        subprocess.run([processor_path, '/home/user/workspace'], check=True)
    finally:
        # 5. Kill the agent's script and inotifywait
        subprocess.run(['pkill', '-f', 'rescue.sh'], capture_output=True)
        subprocess.run(['pkill', '-f', 'inotifywait'], capture_output=True)
        try:
            os.killpg(os.getpgid(agent_proc.pid), 9)
        except Exception:
            pass

    # 6. Run the verifier logic to count valid rescued files
    manifest_path = '/home/user/rescued_data/manifest.txt'
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} was not created."

    valid_count = 0
    seen_hashes = set()

    with open(manifest_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                expected_hash = parts[0]
                filename = parts[1]
                filepath = os.path.join('/home/user/rescued_data', os.path.basename(filename))

                if os.path.exists(filepath) and expected_hash not in seen_hashes:
                    with open(filepath, 'rb') as dat:
                        actual_hash = hashlib.sha256(dat.read()).hexdigest()
                    if actual_hash == expected_hash:
                        seen_hashes.add(expected_hash)
                        valid_count += 1

    assert valid_count >= 850, f"Metric threshold failed: Rescued {valid_count} valid files, expected at least 850."