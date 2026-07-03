# test_final_state.py

import os
import socket
import pytest

def test_frames_extracted_and_deleted():
    """Check that frames are extracted and multiples of 5 are deleted."""
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), f"Frames directory does not exist: {frames_dir}"

    # Check frames 1 to 20
    for i in range(1, 21):
        frame_path = os.path.join(frames_dir, f"frame_{i:03d}.pgm")
        if i % 5 == 0:
            assert not os.path.exists(frame_path), f"Frame {i} should have been deleted (multiple of 5)."
        else:
            assert os.path.exists(frame_path), f"Frame {i} is missing. It should have been extracted."

def query_server(frame_id):
    """Helper to query the TCP server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(('127.0.0.1', 8080))
        s.sendall(f"{frame_id}\n".encode('ascii'))
        data = s.recv(1024).decode('ascii').strip()
    except ConnectionRefusedError:
        pytest.fail("Connection refused. Is the server running on 127.0.0.1:8080?")
    except socket.timeout:
        pytest.fail("Server timed out.")
    finally:
        s.close()
    return data

def test_server_nan_responses():
    """Test that the server responds with NaN for missing frames."""
    for missing_id in [5, 10, 15, 20]:
        response = query_server(missing_id)
        assert response == "NaN", f"Expected 'NaN' for frame {missing_id}, got '{response}'"

def test_server_valid_responses():
    """Test that the server responds with correctly formatted posterior means for valid frames."""
    for valid_id in [1, 2, 11, 16]:
        response = query_server(valid_id)
        assert response != "NaN", f"Expected a float for frame {valid_id}, got 'NaN'"

        # Check if it's a valid float with exactly 2 decimal places
        try:
            val = float(response)
        except ValueError:
            pytest.fail(f"Response '{response}' for frame {valid_id} is not a valid float.")

        parts = response.split('.')
        assert len(parts) == 2, f"Response '{response}' does not have a decimal point."
        assert len(parts[1]) == 2, f"Response '{response}' does not have exactly 2 decimal places."