# test_final_state.py

import os
import socket
import pytest

N = 24

def test_video_stats_file():
    """Verify the video_stats.txt file contains the correct FPS."""
    path = "/home/user/video_stats.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert content == "24\n", f"Expected '24\\n' in {path}, got {repr(content)}"

def test_tcp_server_and_logging():
    """Verify the TCP server correctly processes messages and maintains the rolling window."""
    host = '127.0.0.1'
    port = 9000

    messages = [
        "Hello", # 5
        "こんにちは", # 5
        "A", # 1
    ]
    # Add 27 more messages of length 1 to test window rollover (total 30 messages)
    for i in range(27):
        messages.append(f"{chr(97 + (i % 26))}")

    expected_log_lines = []
    window = []

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            f = s.makefile('rw', encoding='utf-8')
            for msg in messages:
                # Calculate code points
                cp_count = len(msg)
                window.append(cp_count)
                if len(window) > N:
                    window.pop(0)

                expected_sum = sum(window)
                expected_log_lines.append(f"RECV: {cp_count} | WINDOW_SUM: {expected_sum}\n")

                # Send message
                f.write(msg + "\n")
                f.flush()

                # Read response
                response = f.readline()
                assert response == f"{expected_sum}\n", f"Expected response '{expected_sum}\\n' for message '{msg}', got {repr(response)}"
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to TCP server at {host}:{port}")
    except socket.timeout:
        pytest.fail("TCP server timed out or did not respond as expected.")

    # Check log file
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        actual_log_lines = f.readlines()

    # The server might have been tested by the student before, so we check if our expected lines are at the end
    assert len(actual_log_lines) >= len(expected_log_lines), "Log file has fewer lines than expected."

    # Check the last len(expected_log_lines) lines
    recent_log_lines = actual_log_lines[-len(expected_log_lines):]
    assert recent_log_lines == expected_log_lines, "Log file contents do not match the expected format or values."