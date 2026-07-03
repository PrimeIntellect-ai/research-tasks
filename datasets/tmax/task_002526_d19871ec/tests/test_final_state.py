# test_final_state.py
import os
import socket
import subprocess
import time

def send_tcp_request(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((host, port))
        s.sendall(message.encode('utf-8'))
        response = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                break
        return response.decode('utf-8')

def test_cleaned_csv():
    """Test that the cleaned CSV file exists and contains the correctly imputed data."""
    csv_path = "/home/user/cleaned_telemetry.csv"
    assert os.path.isfile(csv_path), f"Missing cleaned CSV file: {csv_path}"

    expected_values = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 850, 750, 650, 550]

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    for i, val in enumerate(expected_values):
        expected_line = f"{i+1},{val}"
        assert expected_line in lines, f"Expected line '{expected_line}' not found in {csv_path}"

def test_tcp_server_schema():
    """Test that the TCP server correctly responds to the SCHEMA command."""
    response = send_tcp_request('127.0.0.1', 9090, "SCHEMA\n")
    expected = "frame_number:int,sensor_value:int\n"
    assert response == expected, f"Unexpected SCHEMA response. Expected {repr(expected)}, got {repr(response)}"

def test_tcp_server_data():
    """Test that the TCP server correctly responds to DATA commands with imputed values."""
    cases = {
        4: 350,
        8: 550,
        14: 850,
        1: 200,
        20: 550
    }
    for frame, expected_val in cases.items():
        response = send_tcp_request('127.0.0.1', 9090, f"DATA {frame}\n")
        expected = f"{expected_val}\n"
        assert response == expected, f"Unexpected DATA {frame} response. Expected {repr(expected)}, got {repr(response)}"

def test_tcp_server_stats():
    """Test that the TCP server correctly responds to the STATS command with bootstrapped statistics."""
    awk_script = """
BEGIN {
    srand(42)
    split("200 250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 850 750 650 550", data, " ")
    n = length(data)
    for(i=1; i<=10000; i++) {
        sum = 0
        for(j=1; j<=n; j++) {
            idx = int(rand() * n) + 1
            sum += data[idx]
        }
        means[i] = sum / n
    }
    asort(means)
    total = 0
    for(i=1; i<=10000; i++) total += means[i]
    mean = total / 10000
    lower = means[250] # 2.5% of 10000
    upper = means[9750] # 97.5% of 10000
    printf "mean:%.2f,lower:%.2f,upper:%.2f\\n", mean, lower, upper
}
"""
    script_path = '/tmp/truth_bootstrap.awk'
    with open(script_path, 'w') as f:
        f.write(awk_script)

    result = subprocess.run(['gawk', '-f', script_path], capture_output=True, text=True)
    expected_stats = result.stdout

    response = send_tcp_request('127.0.0.1', 9090, "STATS\n")
    assert response == expected_stats, f"Unexpected STATS response. Expected {repr(expected_stats)}, got {repr(response)}"