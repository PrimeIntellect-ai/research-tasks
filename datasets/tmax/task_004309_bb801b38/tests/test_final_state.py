# test_final_state.py

import os
import time
import json
import glob
import subprocess
import urllib.request
import urllib.error
import pytest

def test_adversarial_corpus_verification():
    start_script = "/home/user/start_services.sh"
    assert os.path.isfile(start_script), f"Missing start script: {start_script}"
    assert os.access(start_script, os.X_OK), f"Start script is not executable: {start_script}"

    # Start services
    process = subprocess.Popen(["bash", start_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Wait for services to start
        time.sleep(5)

        clean_dir = "/home/user/corpus/clean"
        evil_dir = "/home/user/corpus/evil"

        clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
        evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

        assert len(clean_files) > 0, "No clean corpus files found."
        assert len(evil_files) > 0, "No evil corpus files found."

        expected_results = {}

        def send_payload(filepath, expected_status):
            with open(filepath, 'r') as f:
                data = f.read()
                try:
                    parsed = json.loads(data)
                    graph_id = parsed.get("graph_id")
                    if graph_id is None:
                        # Fallback to filename without extension if graph_id not in JSON
                        graph_id = os.path.splitext(os.path.basename(filepath))[0]
                except json.JSONDecodeError:
                    graph_id = os.path.splitext(os.path.basename(filepath))[0]

            expected_results[str(graph_id)] = expected_status

            req = urllib.request.Request(
                "http://localhost:5000/process",
                data=data.encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            try:
                urllib.request.urlopen(req, timeout=2)
            except Exception as e:
                pytest.fail(f"Failed to send POST request to API for {filepath}: {e}")

        for f in clean_files:
            send_payload(f, "CLEAN")

        for f in evil_files:
            send_payload(f, "EVIL")

        # Wait for Rust worker to process
        time.sleep(5)

        results_file = "/home/user/classification_results.csv"
        assert os.path.isfile(results_file), f"Results file not found: {results_file}"

        actual_results = {}
        with open(results_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 2:
                    actual_results[str(parts[0])] = parts[1].strip().upper()

        evil_bypassed = []
        clean_modified = []

        for graph_id, expected_status in expected_results.items():
            actual_status = actual_results.get(graph_id)
            if expected_status == "EVIL" and actual_status != "EVIL":
                evil_bypassed.append(graph_id)
            elif expected_status == "CLEAN" and actual_status != "CLEAN":
                clean_modified.append(graph_id)

        error_msgs = []
        if evil_bypassed:
            error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

        if error_msgs:
            pytest.fail(" | ".join(error_msgs))

    finally:
        # Cleanup processes
        subprocess.run(["pkill", "-f", "redis-server"], check=False)
        subprocess.run(["pkill", "-f", "api.py"], check=False)
        subprocess.run(["pkill", "-f", "rust_worker"], check=False)
        process.terminate()