# test_final_state.py

import os
import stat
import hashlib

def test_result_log():
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"{log_path} must contain at least two lines."

    expected_password = "secr3t_vault!"
    expected_token = "TOKEN=" + hashlib.md5((expected_password + "_salt123").encode()).hexdigest()

    assert lines[0] == expected_password, f"Line 1 of {log_path} is incorrect. Expected the cracked password."
    assert lines[1] == expected_token, f"Line 2 of {log_path} is incorrect. Expected the generated token."

def test_sandbox_script():
    script_path = "/home/user/sandbox.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "env -i" in content, f"{script_path} must use 'env -i' to clear environment variables."
    assert "PATH=/usr/bin:/usr/local/bin:/bin" in content, f"{script_path} must explicitly set PATH."

    expected_password = "secr3t_vault!"
    expected_token = "TOKEN=" + hashlib.md5((expected_password + "_salt123").encode()).hexdigest()

    assert f"AUTH_TOKEN={expected_token}" in content or f"AUTH_TOKEN='{expected_token}'" in content or f'AUTH_TOKEN="{expected_token}"' in content, f"{script_path} must pass the token as AUTH_TOKEN."
    assert "python3 /home/user/audit/server.py" in content, f"{script_path} must start the python server."

def test_server_csp_header():
    server_path = "/home/user/audit/server.py"
    assert os.path.isfile(server_path), f"File {server_path} is missing."

    with open(server_path, "r") as f:
        content = f.read()

    expected_header1 = "self.send_header('Content-Security-Policy', \"default-src 'self'; script-src 'none';\")"
    expected_header2 = "self.send_header(\"Content-Security-Policy\", \"default-src 'self'; script-src 'none';\")"
    expected_header3 = 'self.send_header(\'Content-Security-Policy\', \'default-src \\\'self\\\'; script-src \\\'none\\\';\')'

    header_found = any(h in content for h in [expected_header1, expected_header2, expected_header3])

    # Alternatively, just check for the presence of the header name and value
    assert "Content-Security-Policy" in content, f"CSP header name missing in {server_path}."
    assert "default-src 'self'; script-src 'none';" in content, f"CSP header value missing or incorrect in {server_path}."