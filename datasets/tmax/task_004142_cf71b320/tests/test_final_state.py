# test_final_state.py
import socket
import os
import pytest

def send_request(host, port, message):
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(message.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        return str(e)

def test_files_exist():
    assert os.path.exists("/home/user/train.sh"), "/home/user/train.sh does not exist"
    assert os.path.exists("/home/user/serve.sh"), "/home/user/serve.sh does not exist"
    assert os.path.exists("/home/user/model.txt"), "/home/user/model.txt does not exist"

def test_auth_failure():
    host, port = "127.0.0.1", 9090
    message = "AUTH:wrong|LOG:login failed admin\n"
    response = send_request(host, port, message)
    assert response == "ERROR: UNAUTHORIZED\n", f"Expected 'ERROR: UNAUTHORIZED\\n', got {repr(response)}"

def test_inference_benign_calculation():
    host, port = "127.0.0.1", 9090
    message = "AUTH:sysresearch_2024|LOG:session opened user\n"
    response = send_request(host, port, message)

    # Expected calculation:
    # M_count = 4, B_count = 3, Total = 7
    # M_words = 12, B_words = 9, Vocab = 17
    # P(M) = 4/7, P(B) = 3/7
    # Log: "session opened user"
    # Score M = (4/7) * ((0+1)/(12+17)) * ((0+1)/(12+17)) * ((1+1)/(12+17)) = 4/7 * 1/29 * 1/29 * 2/29
    # Score B = (3/7) * ((1+1)/(9+17)) * ((1+1)/(9+17)) * ((1+1)/(9+17)) = 3/7 * 2/26 * 2/26 * 2/26
    # Score M = 8 / 170723
    # Score B = 24 / 123032
    # Prob M = Score M / (Score M + Score B) = 0.19369...
    # Rounded to 4 decimal places: 0.1937

    expected = "RESULT:0.1937\n"
    assert response == expected, f"Expected {repr(expected)}, got {repr(response)}"