# test_final_state.py
import socket
import re
import pytest

HOST = "127.0.0.1"
PORT = 8080

def send_request(payload: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            pytest.fail(f"Could not connect to {HOST}:{PORT}. Is the server running?")

        s.sendall(payload.encode('utf-8'))

        response = b""
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    break
                response += data
            except socket.timeout:
                break
    return response.decode('utf-8').strip()

def test_integrate_accuracy():
    """Test that the INTEGRATE command returns the correct numerical result."""
    response = send_request("INTEGRATE 4.0\n")
    assert response, "No response received for INTEGRATE request."

    try:
        val = float(response)
    except ValueError:
        pytest.fail(f"Could not parse response as float: {response!r}")

    expected = 84.2666
    assert abs(val - expected) < 0.05, f"Integration result {val} is not within 0.05 of expected {expected}."

def test_density_formatting():
    """Test that the DENSITY command returns the correctly formatted histogram."""
    response = send_request("DENSITY\n")
    assert response, "No response received for DENSITY request."

    lines = response.strip().split('\n')
    assert len(lines) == 10, f"Expected 10 lines in DENSITY response, got {len(lines)}:\n{response}"

    expected_bins = [
        "0-10", "10-20", "20-30", "30-40", "40-50",
        "50-60", "60-70", "70-80", "80-90", "90-100"
    ]

    total_count = 0
    for i, line in enumerate(lines):
        match = re.match(r"^(\d+-\d+):\s*(\d+)$", line.strip())
        assert match, f"Line {i+1} does not match expected format '[bin_start]-[bin_end]: <count>': {line!r}"
        bin_label, count_str = match.groups()
        assert bin_label == expected_bins[i], f"Expected bin {expected_bins[i]}, got {bin_label}"
        total_count += int(count_str)

    assert total_count == 5000, f"Expected sum of counts to be exactly 5000, got {total_count}"