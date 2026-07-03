# test_final_state.py
import os
import pytest

def test_build_script_exists_and_executable():
    script_path = "/home/user/release/build.sh"
    assert os.path.isfile(script_path), f"Build script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Build script {script_path} is not executable."

def test_applied_patches_log():
    log_path = "/home/user/release/applied_patches.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "patches/add_health.patch",
        "patches/add_metrics.patch",
        "patches/remove_ping.patch"
    ]

    assert lines == expected_lines, (
        f"applied_patches.log contents are incorrect.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {lines}"
    )

def test_final_proto_content():
    proto_path = "/home/user/release/final.proto"
    assert os.path.isfile(proto_path), f"Generated {proto_path} is missing."

    with open(proto_path, "r") as f:
        content = f.read()

    assert "rpc HealthCheck" in content, "final.proto is missing HealthCheck RPC (add_health.patch not applied correctly)."
    assert "rpc GetMetrics" in content, "final.proto is missing GetMetrics RPC (add_metrics.patch not applied correctly)."
    assert "rpc Ping" not in content, "final.proto still contains Ping RPC (remove_ping.patch not applied correctly)."
    assert "rpc LogEvent" not in content, "final.proto contains LogEvent RPC (add_logging.patch should NOT be applied for target 2.0.0)."

def test_grpc_output_files():
    out_dir = "/home/user/release/out"
    assert os.path.isdir(out_dir), f"Output directory {out_dir} is missing."

    pb2_file = os.path.join(out_dir, "final_pb2.py")
    pb2_grpc_file = os.path.join(out_dir, "final_pb2_grpc.py")

    assert os.path.isfile(pb2_file), f"gRPC generated file {pb2_file} is missing."
    assert os.path.isfile(pb2_grpc_file), f"gRPC generated file {pb2_grpc_file} is missing."

def test_venv_exists():
    venv_dir = "/home/user/release/venv"
    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} is missing."

    # Check if python executable exists inside venv
    python_path = os.path.join(venv_dir, "bin", "python")
    assert os.path.isfile(python_path) or os.path.islink(python_path), f"Python executable missing in venv: {python_path}"