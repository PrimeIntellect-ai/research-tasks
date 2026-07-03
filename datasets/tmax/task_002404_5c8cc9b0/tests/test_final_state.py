# test_final_state.py
import os
import csv
import subprocess
import time
import shutil
import tempfile
import pytest

def test_ssh_config_hardened():
    sshd_config_path = "/app/sshd/sshd_config"
    assert os.path.isfile(sshd_config_path), f"Missing file: {sshd_config_path}"

    with open(sshd_config_path, 'r') as f:
        content = f.read()

    # Check for required configurations
    assert "PasswordAuthentication no" in content, "PasswordAuthentication is not explicitly disabled in sshd_config."
    assert "PubkeyAuthentication yes" in content, "PubkeyAuthentication is not enabled in sshd_config."

def test_ssh_keys_generated():
    private_key_path = "/home/user/.ssh/id_rsa"
    authorized_keys_path = "/app/sshd/authorized_keys"

    assert os.path.isfile(private_key_path), f"SSH private key not found at {private_key_path}"
    assert os.path.isfile(authorized_keys_path), f"Authorized keys file not found at {authorized_keys_path}"

def test_flask_app_no_password():
    flask_app_path = "/app/backend/flask_app.py"
    assert os.path.isfile(flask_app_path), f"Missing file: {flask_app_path}"

    with open(flask_app_path, 'r') as f:
        content = f.read()

    assert "supersecret123" not in content, "Hardcoded password still present in flask_app.py"
    assert "--password" not in content, "Password argument still being passed in flask_app.py"

def test_helper_no_password():
    helper_path = "/app/backend/helper.py"
    assert os.path.isfile(helper_path), f"Missing file: {helper_path}"

    with open(helper_path, 'r') as f:
        content = f.read()

    assert "supersecret123" not in content, "Hardcoded password still present in helper.py"
    assert "password=" not in content.replace(" ", ""), "Password authentication appears to be used in helper.py"

def test_ids_filter_adversarial_corpus():
    script_path = "/home/user/ids_filter.py"
    evil_corpus_dir = "/home/user/corpora/evil"
    clean_corpus_dir = "/home/user/corpora/clean"

    assert os.path.isfile(script_path), f"IDS filter script missing at {script_path}"
    assert os.path.isdir(evil_corpus_dir), f"Evil corpus missing at {evil_corpus_dir}"
    assert os.path.isdir(clean_corpus_dir), f"Clean corpus missing at {clean_corpus_dir}"

    with tempfile.TemporaryDirectory() as staging_dir:
        # Copy all evil and clean files into the staging directory
        evil_files = os.listdir(evil_corpus_dir)
        clean_files = os.listdir(clean_corpus_dir)

        for f in evil_files:
            shutil.copy(os.path.join(evil_corpus_dir, f), staging_dir)
        for f in clean_files:
            shutil.copy(os.path.join(clean_corpus_dir, f), staging_dir)

        results_csv = os.path.join(staging_dir, "results.csv")

        # Run the agent's script
        result = subprocess.run(
            ["python3", script_path, staging_dir, results_csv],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"IDS filter script failed with error:\n{result.stderr}"
        assert os.path.isfile(results_csv), f"Output CSV not created at {results_csv}"

        # Parse the CSV
        classifications = {}
        with open(results_csv, 'r') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            assert header == ["filename", "label"], f"Invalid CSV header: {header}"

            for row in reader:
                if len(row) == 2:
                    classifications[row[0]] = row[1]

        # Verify evil corpus
        evil_bypassed = []
        for f in evil_files:
            if classifications.get(f) != "evil":
                evil_bypassed.append(f)

        # Verify clean corpus
        clean_modified = []
        for f in clean_files:
            if classifications.get(f) != "clean":
                clean_modified.append(f)

        error_msgs = []
        if evil_bypassed:
            error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (flagged as evil or missing): {', '.join(clean_modified)}")

        if error_msgs:
            pytest.fail(" | ".join(error_msgs))

def test_end_to_end_services():
    start_script = "/app/start_services.sh"
    assert os.path.isfile(start_script), f"Missing file: {start_script}"

    # Run the start script
    subprocess.run(["bash", start_script], check=True)

    # Wait for services to come up
    time.sleep(2)

    # Trigger the endpoint
    try:
        result = subprocess.run(
            ["curl", "-s", "http://127.0.0.1:8080/trigger"],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0, "Curl command failed to execute."
        assert '{"status": "success"}' in result.stdout, f"Unexpected response from API: {result.stdout}"
    finally:
        # Cleanup: stop services if possible to not interfere with other processes
        subprocess.run(["pkill", "-f", "nginx"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "flask"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "sshd"], stderr=subprocess.DEVNULL)