# test_final_state.py
import subprocess
import json

def test_websocket_server_response():
    """
    Connects to the WebSocket server at 0.0.0.0:8081, sends GET_REPORT,
    and verifies the JSON response exactly matches the expected derived truth.
    """
    cmd = ["websocat", "ws://127.0.0.1:8081"]

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send GET_REPORT and wait for response.
    # We use a timeout to prevent hanging if the server keeps the connection open indefinitely
    # after sending the response.
    try:
        stdout, stderr = proc.communicate(input="GET_REPORT\n", timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()

    output = stdout.strip()
    assert output, f"WebSocket server did not return any output. stderr: {stderr}"

    # Parse the last line of output as JSON
    last_line = output.splitlines()[-1]
    try:
        data = json.loads(last_line)
    except json.JSONDecodeError:
        assert False, f"WebSocket server response is not valid JSON: {last_line}"

    # Verify the contents of the JSON payload
    assert "corrupt_frame" in data, "Response missing 'corrupt_frame' key"
    assert data["corrupt_frame"] == 42, f"Expected corrupt_frame 42, got {data['corrupt_frame']}"

    assert "corrupt_module" in data, "Response missing 'corrupt_module' key"
    assert data["corrupt_module"] == "lib_renderer", f"Expected corrupt_module 'lib_renderer', got {data['corrupt_module']}"

    assert "impacted_deps" in data, "Response missing 'impacted_deps' key"
    expected_deps = ["core_utils", "lib_gl", "lib_math"]
    assert data["impacted_deps"] == expected_deps, f"Expected impacted_deps {expected_deps}, got {data['impacted_deps']}"

    assert "ascii_sum" in data, "Response missing 'ascii_sum' key"
    assert data["ascii_sum"] == 2603, f"Expected ascii_sum 2603, got {data['ascii_sum']}"