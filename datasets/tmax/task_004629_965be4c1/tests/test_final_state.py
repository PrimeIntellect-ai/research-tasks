# test_final_state.py

import os
import socket
import subprocess
import pytest

def get_expected_score(seq, c00, c01, c10, c11):
    cmd = ["/app/legacy_oracle", seq, str(c00), str(c01), str(c10), str(c11)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Legacy oracle failed: {e.stderr}")
    except ValueError:
        pytest.fail(f"Could not parse legacy oracle output: {result.stdout}")

def test_files_exist():
    """Check that the expected source and compiled binary exist."""
    assert os.path.exists("/home/user/sim_server.cpp"), "Source file /home/user/sim_server.cpp is missing."
    assert os.path.exists("/home/user/sim_server"), "Compiled binary /home/user/sim_server is missing."
    assert os.access("/home/user/sim_server", os.X_OK), "/home/user/sim_server is not executable."

@pytest.mark.parametrize("seq, c00, c01, c10, c11", [
    ("A", 1.0, 0.0, 0.0, 1.0),
    ("ACGTACGT", 1.0, 0.5, 0.5, 1.0),
    ("ACGTACGTACGTACGTACGT", 2.0, -0.1, -0.1, 0.5),
    ("GATTACA", 0.8, 0.2, 0.2, 1.2),
])
def test_sim_server_responses(seq, c00, c01, c10, c11):
    """Test the TCP server against the legacy oracle's output."""
    expected = get_expected_score(seq, c00, c01, c10, c11)

    payload = f"{seq},{c00},{c01},{c10},{c11}\n"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10.0)

    try:
        s.connect(("127.0.0.1", 9000))
        s.sendall(payload.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
    except ConnectionRefusedError:
        pytest.fail("Connection refused. Is the server running on 127.0.0.1:9000?")
    except socket.timeout:
        pytest.fail("Server timed out while processing the request.")
    except Exception as e:
        pytest.fail(f"Failed to communicate with server: {e}")
    finally:
        s.close()

    assert response.endswith("\n"), f"Response must end with a newline, got: {repr(response)}"

    try:
        actual = float(response.strip())
    except ValueError:
        pytest.fail(f"Could not parse server response as float: {repr(response)}")

    assert abs(actual - expected) <= 0.001, f"For input {payload.strip()}, expected ~{expected:.4f}, but got {actual:.4f}"