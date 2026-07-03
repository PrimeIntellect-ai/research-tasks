# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def test_monitor_output():
    """Check if the monitor output file exists, is valid JSON, and contains exactly 10 responses."""
    output_path = '/home/user/monitor_output.json'
    assert os.path.exists(output_path), f"Monitor output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("monitor_output.json is not valid JSON.")

    assert isinstance(results, list), "monitor_output.json should contain a JSON array."
    assert len(results) == 10, f"monitor_output.json contains {len(results)} responses instead of 10."

    node1_count = results.count('Node 9001')
    node2_count = results.count('Node 9002')

    assert node1_count > 0, "Load balancing is not distributing requests to Node 9001."
    assert node2_count > 0, "Load balancing is not distributing requests to Node 9002."
    assert node1_count + node2_count == 10, "Unexpected responses found in monitor_output.json."

def test_haproxy_live():
    """Verify that HAProxy is running and load balancing requests."""
    req = urllib.request.Request('http://127.0.0.1:8080/')
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"HAProxy returned status {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body in ['Node 9001', 'Node 9002'], f"HAProxy root returned unexpected body: {body}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to HAProxy on 8080: {e}")

@pytest.mark.parametrize("port", [9001, 9002])
def test_backend_health_live(port):
    """Verify that backend nodes are running and responding to health checks."""
    req = urllib.request.Request(f'http://127.0.0.1:{port}/health')
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Node {port} /health returned status {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == 'OK', f"Node {port} /health returned unexpected body: {body}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to backend health check on {port}: {e}")

def test_git_post_receive_hook():
    """Verify the git post-receive hook exists and is executable."""
    hook_path = '/home/user/backend.git/hooks/post-receive'
    assert os.path.exists(hook_path), f"Git post-receive hook is missing at {hook_path}."
    assert os.path.isfile(hook_path), f"{hook_path} is not a file."
    assert os.access(hook_path, os.X_OK), f"Git post-receive hook at {hook_path} is not executable."