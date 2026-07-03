# test_final_state.py
import os
import urllib.request
import concurrent.futures

def test_fix_log_exists_and_content():
    log_path = "/home/user/fix.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "Service Restored", f"Expected 'Service Restored' in {log_path}, got '{content}'."

def test_tunnel_sh_exists_and_content():
    tunnel_path = "/home/user/tunnel.sh"
    assert os.path.isfile(tunnel_path), f"Tunnel script {tunnel_path} does not exist."
    with open(tunnel_path, "r") as f:
        content = f.read()
    assert "8080" in content and "9999" in content, f"Expected port forwarding command involving ports 8080 and 9999 in {tunnel_path}."

def test_nginx_load_success_rate():
    def fetch_url(url):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200 and response.read().decode('utf-8').strip() == "success":
                    return 1
        except Exception:
            pass
        return 0

    url = "http://127.0.0.1:8080/test.txt"
    successes = 0
    total = 100

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = [executor.submit(fetch_url, url) for _ in range(total)]
        for f in concurrent.futures.as_completed(results):
            successes += f.result()

    success_rate = successes / total
    assert success_rate >= 0.98, f"Metric threshold failed. Success rate {success_rate} < 0.98. The server is not responding correctly or is failing under load."