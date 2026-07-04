# test_final_state.py
import os
import json
import subprocess

def test_webhook_manifest():
    path = "/home/user/manifests/webhook.json"
    assert os.path.isfile(path), f"Webhook manifest {path} is missing."
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Webhook manifest {path} is not valid JSON."

    assert data.get("name") == "webhook", "Webhook name incorrect in manifest."
    assert data.get("command") == "python3 -m http.server 8080 --directory /home/user/public", "Webhook command incorrect in manifest."
    assert data.get("depends_on") == ["backend"], "Webhook dependencies incorrect in manifest."

def test_start_order():
    path = "/home/user/start_order.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the generated launcher?"
    with open(path, "r") as f:
        content = f.read()

    # The task asks to echo the name of each service, e.g., 'echo "Starting db"' or similar.
    # We will extract the service names from the file by checking which service names appear in which order.
    # The required services are: db, backend, frontend, webhook
    lines = [line.strip() for line in content.split('\n') if line.strip()]

    def find_index_of_service(service_name):
        for i, line in enumerate(lines):
            # Split by whitespace and check if the exact word is there, or if the line ends with the word
            if service_name in line.split():
                return i
        return -1

    db_idx = find_index_of_service("db")
    backend_idx = find_index_of_service("backend")
    frontend_idx = find_index_of_service("frontend")
    webhook_idx = find_index_of_service("webhook")

    assert db_idx != -1, "Service 'db' was not found in start_order.txt"
    assert backend_idx != -1, "Service 'backend' was not found in start_order.txt"
    assert frontend_idx != -1, "Service 'frontend' was not found in start_order.txt"
    assert webhook_idx != -1, "Service 'webhook' was not found in start_order.txt"

    assert db_idx < backend_idx, "Dependency ordering failed: 'db' must start before 'backend'"
    assert backend_idx < frontend_idx, "Dependency ordering failed: 'backend' must start before 'frontend'"
    assert backend_idx < webhook_idx, "Dependency ordering failed: 'backend' must start before 'webhook'"

def test_storage_quota():
    data_dir = "/home/user/data"
    test_file = os.path.join(data_dir, "test_huge.dat")
    log_path = "/home/user/operator.log"

    try:
        # Create a file slightly larger than 1024000 bytes
        with open(test_file, "wb") as f:
            f.write(b"0" * 1025000)

        # Clear log if it exists
        if os.path.exists(log_path):
            os.remove(log_path)

        result = subprocess.run(["python3", "/home/user/operator.py"], capture_output=True)
        assert result.returncode == 2, f"Expected exit code 2 when storage quota is exceeded, got {result.returncode}"

        assert os.path.isfile(log_path), f"Log file {log_path} missing after quota exceeded."
        with open(log_path, "r") as f:
            log_content = f.read().strip()
        assert "STORAGE_QUOTA_EXCEEDED" in log_content.split('\n'), f"Log file did not contain exactly 'STORAGE_QUOTA_EXCEEDED'. Got: {log_content}"
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

def test_circular_dependency():
    manifests_dir = "/home/user/manifests"
    bad1 = os.path.join(manifests_dir, "bad1.json")
    bad2 = os.path.join(manifests_dir, "bad2.json")
    log_path = "/home/user/operator.log"

    try:
        with open(bad1, "w") as f:
            json.dump({"name": "bad1", "command": "sleep 1", "depends_on": ["bad2"]}, f)
        with open(bad2, "w") as f:
            json.dump({"name": "bad2", "command": "sleep 1", "depends_on": ["bad1"]}, f)

        # Clear log if it exists
        if os.path.exists(log_path):
            os.remove(log_path)

        result = subprocess.run(["python3", "/home/user/operator.py"], capture_output=True)
        assert result.returncode == 1, f"Expected exit code 1 for circular dependency, got {result.returncode}"

        assert os.path.isfile(log_path), f"Log file {log_path} missing after circular dependency."
        with open(log_path, "r") as f:
            log_content = f.read().strip()
        assert "CIRCULAR_DEPENDENCY" in log_content.split('\n'), f"Log file did not contain exactly 'CIRCULAR_DEPENDENCY'. Got: {log_content}"
    finally:
        if os.path.exists(bad1):
            os.remove(bad1)
        if os.path.exists(bad2):
            os.remove(bad2)