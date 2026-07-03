# test_final_state.py

import os
import socket
import pytest

def test_dashboard_result():
    target_dir = "/home/user/target_logs"
    total_size = 0
    if os.path.exists(target_dir):
        for root, dirs, files in os.walk(target_dir):
            for f in files:
                total_size += os.path.getsize(os.path.join(root, f))
    else:
        pytest.fail(f"Target directory {target_dir} does not exist.")

    expected_content = f"Target: {target_dir}, Size: {total_size}"

    result_file = "/home/user/dashboard_result.txt"
    assert os.path.exists(result_file), f"{result_file} does not exist. The dashboard script must create this file."

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {result_file} is incorrect.\nExpected: '{expected_content}'\nGot: '{content}'"

def test_port_forwarding():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(("127.0.0.1", 9090))
        data = s.recv(1024).decode("utf-8")
        assert "Passcode:" in data, "Did not receive 'Passcode:' prompt from port 9090. Port forwarding might be misconfigured."

        s.sendall(b"obs_secure_123\n")
        data = s.recv(1024).decode("utf-8")
        assert "Action:" in data, "Did not receive 'Action:' prompt from port 9090 after sending passcode."

        s.sendall(b"CHECK_FS\n")
        data = s.recv(1024).decode("utf-8")
        assert "/home/user/target_logs" in data, "Did not receive correct directory path from port 9090 after sending CHECK_FS."
    except ConnectionRefusedError:
        pytest.fail("Connection refused on 127.0.0.1:9090. Port forwarding is not active.")
    except Exception as e:
        pytest.fail(f"Port forwarding on 9090 failed or daemon interaction failed: {e}")
    finally:
        s.close()

def test_scripts_exist():
    assert os.path.exists("/home/user/dashboard.py"), "/home/user/dashboard.py does not exist."
    assert os.path.exists("/home/user/health_check.py") or os.path.exists("/home/user/health_check.exp"), \
        "Neither /home/user/health_check.py nor /home/user/health_check.exp exists. The interactive automation script is missing."