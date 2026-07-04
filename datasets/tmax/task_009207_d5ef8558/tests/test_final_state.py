# test_final_state.py

import os
import socket

def test_result_file_exists_and_correct():
    result_file = "/home/user/result.txt"
    assert os.path.exists(result_file), f"Result file {result_file} is missing."
    assert os.path.isfile(result_file), f"{result_file} is not a file."

    with open(result_file, "r") as f:
        content = f.read()

    assert "PONG_SUCCESS_8472" in content, "The result.txt file does not contain the expected response 'PONG_SUCCESS_8472'."

def test_bridge_script_exists():
    bridge_script = "/home/user/bridge.py"
    assert os.path.exists(bridge_script), f"Bridge script {bridge_script} is missing."
    assert os.path.isfile(bridge_script), f"{bridge_script} is not a file."

def test_bridge_is_running_and_functional():
    # Test if the bridge is listening on 127.0.0.1:8888 and forwards data correctly
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", 8888))
        s.sendall(b"PING")
        data = s.recv(1024)
        s.close()
    except ConnectionRefusedError:
        raise AssertionError("Connection refused to 127.0.0.1:8888. Is the bridge running?")
    except socket.timeout:
        raise AssertionError("Connection to 127.0.0.1:8888 timed out.")
    except Exception as e:
        raise AssertionError(f"Failed to connect and communicate with the bridge: {e}")

    assert b"PONG_SUCCESS_8472" in data, f"Expected 'PONG_SUCCESS_8472' from bridge, got {data}"