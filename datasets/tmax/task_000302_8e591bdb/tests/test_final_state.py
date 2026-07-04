# test_final_state.py
import os
import subprocess

def test_source_file_exists():
    assert os.path.isfile("/home/user/auth_api.cpp"), "/home/user/auth_api.cpp does not exist."

def test_binary_exists_and_executable():
    assert os.path.isfile("/home/user/auth_api"), "Compiled binary /home/user/auth_api does not exist."
    assert os.access("/home/user/auth_api", os.X_OK), "/home/user/auth_api is not executable."

def test_auth_api_output_sysadmin():
    cmd = ["/home/user/auth_api", "sysadmin:1715000000"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}"

    output = result.stdout
    expected_body = '{"username": "sysadmin", "token": 964796}'

    assert "HTTP/1.1 200 OK" in output, "Missing or incorrect HTTP status line."
    assert "Content-Type: application/json" in output, "Missing or incorrect Content-Type header."
    assert expected_body in output, f"Expected JSON body '{expected_body}' not found in output."

    # Check for blank line separation
    headers_and_body = output.replace('\r\n', '\n').split('\n\n')
    assert len(headers_and_body) >= 2, "Missing blank line between headers and body."
    assert expected_body in headers_and_body[-1], "JSON body is not correctly placed after the blank line."

def test_auth_api_output_testuser():
    # Calculate truth dynamically or use precalculated
    # testuser: 116*1 + 101*2 + 115*3 + 116*4 + 117*5 + 115*6 + 101*7 + 114*8 = 4021
    # 4021 * 1234567890 = 4964197485690
    # 4964197485690 % 999983 = 907086

    cmd = ["/home/user/auth_api", "testuser:1234567890"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}"

    output = result.stdout
    expected_body = '{"username": "testuser", "token": 907086}'

    assert "HTTP/1.1 200 OK" in output, "Missing or incorrect HTTP status line."
    assert "Content-Type: application/json" in output, "Missing or incorrect Content-Type header."
    assert expected_body in output, f"Expected JSON body '{expected_body}' not found in output."