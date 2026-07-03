# test_final_state.py
import os

WORKSPACE_DIR = "/home/user/deploy-manager"

def test_go_mod_exists():
    go_mod_path = os.path.join(WORKSPACE_DIR, "go.mod")
    assert os.path.isfile(go_mod_path), f"Expected {go_mod_path} to exist."
    with open(go_mod_path, "r") as f:
        content = f.read()
    assert "module deploy-manager" in content, "go.mod does not contain the expected module name 'deploy-manager'."

def test_grpc_code_generated():
    pb_go_path = os.path.join(WORKSPACE_DIR, "pb", "rollout.pb.go")
    grpc_go_path = os.path.join(WORKSPACE_DIR, "pb", "rollout_grpc.pb.go")
    assert os.path.isfile(pb_go_path), f"Expected generated protobuf code at {pb_go_path} to exist."
    assert os.path.isfile(grpc_go_path), f"Expected generated gRPC code at {grpc_go_path} to exist."

def test_server_go_exists():
    server_go_path = os.path.join(WORKSPACE_DIR, "server.go")
    assert os.path.isfile(server_go_path), f"Expected {server_go_path} to exist."

def test_test_results_log_exists_and_passed():
    log_path = os.path.join(WORKSPACE_DIR, "test_results.log")
    assert os.path.isfile(log_path), f"Expected test results log at {log_path} to exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "PASS" in content, "The test results log does not contain 'PASS', indicating the tests did not pass successfully."
    assert "TestRolloutService" in content, "The test results log does not appear to contain the output of the TestRolloutService."