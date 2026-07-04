# test_final_state.py

import os
import subprocess
import time
import threading
import pytest

PASSPHRASE_FILE = "/home/user/leaked_passphrase.txt"
EXPECTED_PASSPHRASE = "Omega$hield2024"
RUST_PROJECT_DIR = "/home/user/rusty_scanner"
RUST_BIN = os.path.join(RUST_PROJECT_DIR, "target/debug/rusty_scanner")
SSH_CONFIG = "/home/user/.ssh/config"

def test_passphrase_extracted():
    assert os.path.isfile(PASSPHRASE_FILE), f"Passphrase file missing at {PASSPHRASE_FILE}"
    with open(PASSPHRASE_FILE, "r") as f:
        content = f.read().strip()
    assert content == EXPECTED_PASSPHRASE, f"Expected passphrase '{EXPECTED_PASSPHRASE}', got '{content}'"

def test_ssh_config_hardened():
    assert os.path.isfile(SSH_CONFIG), f"SSH config missing at {SSH_CONFIG}"
    with open(SSH_CONFIG, "r") as f:
        content = f.read().lower()

    assert "permitrootlogin no" in content, "SSH config must disable root login (PermitRootLogin no)"
    assert "passwordauthentication no" in content, "SSH config must enforce key-based auth (PasswordAuthentication no)"

def test_rust_compiles():
    result = subprocess.run(
        ["cargo", "build"],
        cwd=RUST_PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"Rust project failed to compile:\n{result.stderr.decode()}"
    assert os.path.isfile(RUST_BIN), f"Compiled binary not found at {RUST_BIN}"

def test_rust_permission_check(tmp_path):
    # Ensure binary exists
    if not os.path.isfile(RUST_BIN):
        subprocess.run(["cargo", "build"], cwd=RUST_PROJECT_DIR, check=True)

    dummy_key = tmp_path / "id_rsa_test"
    dummy_key.write_text("dummy key content")

    # Test with 0644
    dummy_key.chmod(0o644)
    result_644 = subprocess.run(
        [RUST_BIN, "--key", str(dummy_key), "--passphrase", "test", "--target", "127.0.0.1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result_644.returncode != 0, "Scanner should abort when key file permissions are 0644"

def test_leak_rate():
    # Ensure binary exists
    if not os.path.isfile(RUST_BIN):
        subprocess.run(["cargo", "build"], cwd=RUST_PROJECT_DIR, check=True)

    test_passphrase = "SuperSecretTestPassphrase123!"
    num_runs = 50
    leaks_detected = 0

    # Create a valid key to bypass permission check
    dummy_key = "/tmp/valid_id_rsa"
    with open(dummy_key, "w") as f:
        f.write("dummy")
    os.chmod(dummy_key, 0o600)

    stop_event = threading.Event()

    def monitor_proc():
        nonlocal leaks_detected
        while not stop_event.is_set():
            try:
                for pid in os.listdir("/proc"):
                    if pid.isdigit():
                        cmdline_path = f"/proc/{pid}/cmdline"
                        if os.path.isfile(cmdline_path):
                            with open(cmdline_path, "rb") as f:
                                cmdline = f.read()
                                if test_passphrase.encode() in cmdline and b"rusty_scanner" not in cmdline:
                                    leaks_detected += 1
            except Exception:
                pass
            time.sleep(0.01)

    monitor_thread = threading.Thread(target=monitor_proc)
    monitor_thread.start()

    for _ in range(num_runs):
        subprocess.run(
            [RUST_BIN, "--key", dummy_key, "--passphrase", test_passphrase, "--target", "127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    stop_event.set()
    monitor_thread.join()

    leak_rate = leaks_detected / num_runs
    assert leak_rate <= 0.0, f"Metric leak_rate {leak_rate} > threshold 0.0. Passphrase leaked {leaks_detected} times out of {num_runs} runs."