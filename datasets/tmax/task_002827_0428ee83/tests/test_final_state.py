import os
import urllib.request
import urllib.error
import json
import time
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

def test_deployment_log():
    log_path = "/home/user/deployment.log"
    assert os.path.isfile(log_path), f"File not found: {log_path}"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "DEPLOYMENT READY" in content, f"Expected 'DEPLOYMENT READY' in {log_path}"

def test_nginx_running():
    # Check if port 8000 is open
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 8000))
        s.close()
    except ConnectionRefusedError:
        assert False, "Nginx (or a proxy) is not listening on 127.0.0.1:8000"

class DummyLegacyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"legacy": "response"}')

    def log_message(self, format, *args):
        pass

def test_routing_and_green_logic():
    # Start dummy legacy server on 8080
    legacy_server = HTTPServer(('127.0.0.1', 8080), DummyLegacyHandler)
    server_thread = threading.Thread(target=legacy_server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(0.5)

    try:
        # Test 1: Fallback routing to legacy (no header)
        req = urllib.request.Request("http://127.0.0.1:8000/get/test")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                body = response.read().decode('utf-8')
                assert "legacy" in body, "Expected response from legacy server on port 8080 when missing X-Deploy-Env header"
        except Exception as e:
            assert False, f"Failed to reach legacy server through proxy: {e}"

        # Helper for green requests
        def green_post(path, data=None):
            req = urllib.request.Request(f"http://127.0.0.1:8000{path}", method="POST")
            req.add_header("X-Deploy-Env", "green")
            if data:
                req.add_header("Content-Type", "application/json")
                req.data = json.dumps(data).encode('utf-8')
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        res_body = response.read().decode('utf-8')
                        return json.loads(res_body) if res_body else {}
                    return None
            except urllib.error.HTTPError as e:
                return {"error": e.code}
            except Exception as e:
                assert False, f"Green POST {path} failed: {e}"

        def green_get(path):
            req = urllib.request.Request(f"http://127.0.0.1:8000{path}")
            req.add_header("X-Deploy-Env", "green")
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    return json.loads(response.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                return {"error": e.code}
            except Exception as e:
                assert False, f"Green GET {path} failed: {e}"

        # Test 2: Put items
        green_post("/put", {"key": "A", "value": "valA", "priority": 10})
        green_post("/put", {"key": "B", "value": "valB", "priority": 10})
        green_post("/put", {"key": "C", "value": "valC", "priority": 5})
        green_post("/put", {"key": "D", "value": "valD", "priority": 5})

        # Test 3: Evict lowest priority (5), LIFO order (D was most recently added among priority 5)
        evict1 = green_post("/evict")
        assert evict1 is not None and "key" in evict1, "Evict response missing key"
        assert evict1["key"] == "D", f"Expected to evict 'D', got {evict1['key']}"

        # Test 4: Evict next lowest priority (5), LIFO order (C is remaining)
        evict2 = green_post("/evict")
        assert evict2 is not None and "key" in evict2, "Evict response missing key"
        assert evict2["key"] == "C", f"Expected to evict 'C', got {evict2['key']}"

        # Test 5: Get A
        get_a = green_get("/get/A")
        assert get_a is not None and "value" in get_a, "Get A response missing value"
        assert get_a["value"] == "valA", f"Expected value 'valA', got {get_a['value']}"

    finally:
        legacy_server.shutdown()
        legacy_server.server_close()