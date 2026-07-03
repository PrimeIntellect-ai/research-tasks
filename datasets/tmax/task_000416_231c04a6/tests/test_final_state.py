# test_final_state.py
import os
import sys
import json
import socket
import importlib.util

def test_memory_fix_log_exists():
    """Check if the memory fix log was created."""
    log_path = "/home/user/memory_fix_log.txt"
    assert os.path.isfile(log_path), f"{log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert len(content) > 0, f"{log_path} is empty."

def test_artifact_graph_leak_fixed():
    """Check if artifact_graph.py uses weakref or breaks cycles."""
    graph_path = "/home/user/artifact_graph.py"
    assert os.path.isfile(graph_path), f"{graph_path} is missing."
    with open(graph_path, "r") as f:
        content = f.read()
    # A proper fix usually involves weakref or avoiding the dependents list
    # We will just verify the file has been modified from the original
    assert "node.dependents.append(self)" not in content or "weakref" in content, \
        "The circular reference in artifact_graph.py does not appear to be fixed (e.g., using weakref)."

def test_artifact_graph_logic():
    """Check if BuildGraph still computes the correct build order."""
    sys.path.insert(0, "/home/user")
    import artifact_graph

    bg = artifact_graph.BuildGraph()
    bg.add_artifact("A", [])
    bg.add_artifact("B", ["A"])
    bg.add_artifact("C", ["A"])
    bg.add_artifact("D", ["B", "C"])

    order = bg.get_build_order()
    assert order[0] == "A", "Build order must start with A"
    assert "D" == order[-1], "Build order must end with D"
    assert set(order) == {"A", "B", "C", "D"}, "Build order must contain all artifacts"

def test_protobuf_files_exist():
    """Check if the protobuf definitions and compiled files exist."""
    proto_path = "/home/user/build_service.proto"
    assert os.path.isfile(proto_path), f"{proto_path} is missing."

    with open(proto_path, "r") as f:
        content = f.read()
    assert "syntax = \"proto3\";" in content, "Proto file must use proto3 syntax."
    assert "message Artifact" in content, "Proto file must define Artifact message."
    assert "message GraphRequest" in content, "Proto file must define GraphRequest message."
    assert "message OrderResponse" in content, "Proto file must define OrderResponse message."
    assert "service BuildResolver" in content, "Proto file must define BuildResolver service."

    pb2_path = "/home/user/build_service_pb2.py"
    pb2_grpc_path = "/home/user/build_service_pb2_grpc.py"
    assert os.path.isfile(pb2_path), f"Compiled protobuf file {pb2_path} is missing."
    assert os.path.isfile(pb2_grpc_path), f"Compiled gRPC file {pb2_grpc_path} is missing."

def test_server_pid_and_ports():
    """Check if the server is running and listening on the required ports."""
    pid_path = "/home/user/server.pid"
    assert os.path.isfile(pid_path), f"{pid_path} is missing. Server might not be running in the background."

    with open(pid_path, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"

    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running."

    # Check gRPC port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 50051))
        assert result == 0, "gRPC server is not listening on port 50051."

    # Check WebSocket port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 8765))
        assert result == 0, "WebSocket server is not listening on port 8765."