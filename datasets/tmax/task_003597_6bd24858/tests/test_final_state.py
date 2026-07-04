# test_final_state.py
import os
import subprocess

def test_url_tool_compiled_and_tests_pass():
    tool_path = '/home/user/url_tool'
    assert os.path.exists(tool_path), f"Compiled binary {tool_path} does not exist."
    assert os.access(tool_path, os.X_OK), f"{tool_path} is not executable."

    result = subprocess.run([tool_path, '--test'], capture_output=True, text=True)
    assert result.returncode == 0, f"url_tool --test failed with exit code {result.returncode}. Stderr: {result.stderr}"
    assert "PASS" in result.stdout, f"url_tool --test did not print 'PASS'. Output: {result.stdout}"

def test_matches_txt_contents():
    matches_path = '/home/user/matches.txt'
    assert os.path.exists(matches_path), f"{matches_path} does not exist."

    with open(matches_path, 'r') as f:
        matches = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "/admin/config?a=b",
        "/etc/passwd",
        "/vulnerable path"
    ]

    assert sorted(matches) == sorted(expected), f"Contents of {matches_path} do not match expected known bad paths. Found: {matches}"

def test_nginx_proxy_conf():
    conf_path = '/home/user/proxy.conf'
    assert os.path.exists(conf_path), f"{conf_path} does not exist."

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "daemon off;" in content, f"{conf_path} is missing 'daemon off;' directive."
    assert "listen 127.0.0.1:8080;" in content or "listen 8080;" in content and "127.0.0.1" in content, f"{conf_path} does not seem to listen on 127.0.0.1:8080."
    assert "proxy_pass http://127.0.0.1:9000;" in content or "proxy_pass http://127.0.0.1:9000" in content, f"{conf_path} is missing the proxy_pass directive to http://127.0.0.1:9000."
    assert "access_log /home/user/access.log;" in content, f"{conf_path} is missing 'access_log /home/user/access.log;' directive."
    assert "pid /home/user/nginx.pid;" in content, f"{conf_path} is missing 'pid /home/user/nginx.pid;' directive."
    assert "user " not in content, f"{conf_path} should not contain a 'user' directive."