# test_final_state.py

import socket
import pytest

HOST = '127.0.0.1'
PORT = 7070

def send_and_receive(payload: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            pytest.fail(f"Could not connect to TCP server at {HOST}:{PORT}. Is it running?")

        s.sendall(payload.encode('utf-8'))
        s.shutdown(socket.SHUT_WR)

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

        return response.decode('utf-8')

def test_tcp_server_basic_aggregation():
    """Test the server with a standard payload containing matching and non-matching edges."""
    payload = (
        "A,B,PURCHASE,100\n"
        "C,D,REFUND,50\n"
        "A,E,REFUND,200\n"
        "C,F,REFUND,300\n"
        "B,G,PURCHASE,500\n"
    )
    expected_response = "MAX_SOURCE: C, AMOUNT: 350\n"

    actual_response = send_and_receive(payload)
    assert actual_response == expected_response, (
        f"Expected response {repr(expected_response)}, but got {repr(actual_response)}"
    )

def test_tcp_server_no_matching_edges():
    """Test the server when there are no matching edges in the payload."""
    payload = (
        "A,B,PURCHASE,100\n"
        "B,G,PURCHASE,500\n"
    )
    expected_response = "MAX_SOURCE: NONE, AMOUNT: 0\n"

    actual_response = send_and_receive(payload)
    assert actual_response == expected_response, (
        f"Expected response {repr(expected_response)} for no matching edges, but got {repr(actual_response)}"
    )

def test_tcp_server_empty_payload():
    """Test the server with an empty payload."""
    payload = ""
    expected_response = "MAX_SOURCE: NONE, AMOUNT: 0\n"

    actual_response = send_and_receive(payload)
    assert actual_response == expected_response, (
        f"Expected response {repr(expected_response)} for empty payload, but got {repr(actual_response)}"
    )