# test_final_state.py
import os

def test_server_fixed_go():
    path = "/home/user/server_fixed.go"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    expected_header = "default-src 'self'; script-src 'none';"
    assert "Content-Security-Policy" in content, "Content-Security-Policy header is missing in server_fixed.go."
    assert expected_header in content, f"The CSP header value should be exactly: {expected_header}"
    assert "<html><body><h1>Admin Dashboard</h1></body></html>" in content, "The original HTTP response body must not be changed."

def test_decrypted_secret():
    path = "/home/user/decrypted_secret.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you successfully decrypt the secret?"

    with open(path, "r") as f:
        content = f.read()

    expected_secret = "FLAG{aud1t_p4ss3d_c5p_a3s}"
    assert content == expected_secret, f"The decrypted secret is incorrect. Expected exactly '{expected_secret}', but got '{content}'."