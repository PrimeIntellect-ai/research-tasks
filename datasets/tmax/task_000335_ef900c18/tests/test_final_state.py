# test_final_state.py

import socket
import os

def test_reducer_compiled():
    """Verify that the reducer binary has been compiled."""
    assert os.path.isfile("/app/artifact_pca/reducer"), "The reducer binary was not compiled (missing /app/artifact_pca/reducer)"
    assert os.access("/app/artifact_pca/reducer", os.X_OK), "The reducer file is not executable"

def test_tcp_service_response():
    """Verify that the service is running on port 8888 and returns the correct projection."""
    host = '127.0.0.1'
    port = 8888

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            # Send the test payload
            payload = b"EMBEDDING:1.5,2.5,3.5,4.5\n"
            s.sendall(payload)

            # Receive the response
            response = s.recv(1024)
            assert response, "No response received from the service"

            response_str = response.decode('utf-8', errors='replace')
            expected_output = "PROJECTION:4.00,8.00"

            assert expected_output in response_str, f"Expected '{expected_output}' in response, but got: {response_str.strip()}"

    except ConnectionRefusedError:
        assert False, f"Connection refused on {host}:{port}. Is the TCP service running?"
    except socket.timeout:
        assert False, "Connection timed out. The service did not respond in time."
    except Exception as e:
        assert False, f"An error occurred while communicating with the service: {e}"