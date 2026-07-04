# test_final_state.py
import os

def test_generated_files_exist():
    """Verify that the protobuf files were successfully compiled."""
    assert os.path.isfile("/home/user/project/service_pb2.py"), "service_pb2.py was not generated. Did you compile the protobuf schema?"
    assert os.path.isfile("/home/user/project/service_pb2_grpc.py"), "service_pb2_grpc.py was not generated. Did you compile the protobuf schema?"

def test_proxy_results_log():
    """Verify that the proxy results log contains the correct output from the test client."""
    log_path = "/home/user/project/proxy_results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in proxy_results.log, found {len(lines)}. Did you run the test client?"

    # We check the last two lines in case the user ran the client multiple times
    last_two_lines = lines[-2:]
    assert last_two_lines[0] == "REJECTED: Version too low", f"Expected first request to be rejected, but got: {last_two_lines[0]}"
    assert last_two_lines[1] == "SUCCESS: Forwarded message to WS", f"Expected second request to be accepted (2.10.0 > 2.2.0), but got: {last_two_lines[1]}"