# test_final_state.py

import os
import time
import tarfile
import tempfile
import subprocess

def create_archive(tar_path, app_name, version, payload_content):
    with tempfile.TemporaryDirectory() as tmpdir:
        manifest_path = os.path.join(tmpdir, "manifest.txt")
        with open(manifest_path, "w") as f:
            f.write(f"AppName: {app_name}\nVersion: {version}\n")

        payload_path = os.path.join(tmpdir, "payload.bin")
        with open(payload_path, "w") as f:
            f.write(payload_content)

        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(manifest_path, arcname="manifest.txt")
            tar.add(payload_path, arcname="payload.bin")

def test_artifact_manager_behavior():
    # 1. Check readiness
    status_file = "/home/user/curator/status.txt"
    assert os.path.exists(status_file), "status.txt was not created"
    with open(status_file, "r") as f:
        status = f.read().strip()
    assert status == "READY", f"status.txt does not contain READY, got '{status}'"

    incoming_dir = "/home/user/incoming"
    repo_dir = "/home/user/repo"

    assert os.path.isdir(incoming_dir), "incoming directory does not exist"
    assert os.path.isdir(repo_dir), "repo directory does not exist"

    # 2. Drop archives
    archive1_path = os.path.join(incoming_dir, "upload_abc123.tar.gz")
    create_archive(archive1_path, "backend", "2.1.0", "dummy payload")
    time.sleep(1)

    archive2_path = os.path.join(incoming_dir, "upload_def456.tar.gz")
    create_archive(archive2_path, "backend", "2.1.1", "dummy payload 2")
    time.sleep(1)

    archive3_path = os.path.join(incoming_dir, "upload_ghi789.tar.gz")
    create_archive(archive3_path, "worker", "1.0.5", "worker payload")
    time.sleep(2)

    # 3. Trigger shutdown
    shutdown_path = os.path.join(incoming_dir, "SHUTDOWN.txt")
    with open(shutdown_path, "w") as f:
        f.write("shutdown")

    # Wait for processing and shutdown
    time.sleep(3)

    # 4. Verifications
    backend_210 = os.path.join(repo_dir, "backend", "backend-2.1.0.tar.gz")
    assert os.path.isfile(backend_210), f"Missing {backend_210}"

    backend_211 = os.path.join(repo_dir, "backend", "backend-2.1.1.tar.gz")
    assert os.path.isfile(backend_211), f"Missing {backend_211}"

    worker_105 = os.path.join(repo_dir, "worker", "worker-1.0.5.tar.gz")
    assert os.path.isfile(worker_105), f"Missing {worker_105}"

    # 5. Check symlinks
    backend_latest = os.path.join(repo_dir, "backend", "latest.tar.gz")
    assert os.path.islink(backend_latest), f"{backend_latest} is not a symlink"
    backend_target = os.readlink(backend_latest)
    assert backend_target == "backend-2.1.1.tar.gz", f"backend symlink incorrect. Expected backend-2.1.1.tar.gz, got {backend_target}"

    worker_latest = os.path.join(repo_dir, "worker", "latest.tar.gz")
    assert os.path.islink(worker_latest), f"{worker_latest} is not a symlink"
    worker_target = os.readlink(worker_latest)
    assert worker_target == "worker-1.0.5.tar.gz", f"worker symlink incorrect. Expected worker-1.0.5.tar.gz, got {worker_target}"

    # 6. Verify incoming directory is empty of tarballs
    incoming_files = os.listdir(incoming_dir)
    tarballs_left = [f for f in incoming_files if f.endswith(".tar.gz")]
    assert len(tarballs_left) == 0, f"Tarballs left in incoming directory: {tarballs_left}"