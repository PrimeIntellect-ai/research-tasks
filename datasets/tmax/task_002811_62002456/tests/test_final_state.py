# test_final_state.py
import os
import sys
import tempfile
import subprocess
import grpc

def test_files_exist():
    assert os.path.isfile("/home/user/evaluator.proto"), "File /home/user/evaluator.proto is missing"
    assert os.path.isfile("/home/user/server.py"), "File /home/user/server.py is missing"
    assert os.path.isfile("/home/user/test_pbt.py"), "File /home/user/test_pbt.py is missing"

def test_grpc_server_accuracy():
    proto_path = "/home/user/evaluator.proto"
    assert os.path.isfile(proto_path), "evaluator.proto does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        # Compile the protobuf file to the temporary directory
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"--proto_path={os.path.dirname(proto_path)}",
            f"--python_out={tmpdir}",
            f"--grpc_python_out={tmpdir}",
            proto_path
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            assert False, f"Failed to compile protobuf:\n{e.stderr}"

        # Import the generated modules
        sys.path.insert(0, tmpdir)
        try:
            import evaluator_pb2
            import evaluator_pb2_grpc
        except ImportError as e:
            assert False, f"Failed to import generated protobuf modules: {e}"
        finally:
            sys.path.pop(0)

        channel = grpc.insecure_channel('localhost:50051')
        stub = evaluator_pb2_grpc.EvaluatorStub(channel)

        test_cases = [
            {"expr": "A + B * C", "data": {"A": 2, "B": 3, "C": 4}, "expected": 14},
            {"expr": "(A + B) * C", "data": {"A": 2, "B": 3, "C": 4}, "expected": 20},
            {"expr": "Z * Z - Y", "data": {"Z": 10, "Y": 5}, "expected": 95},
            {"expr": "A * (B - C) + D", "data": {"A": 5, "B": 10, "C": 2, "D": 1}, "expected": 41},
            {"expr": "X * Y * Z", "data": {"X": 2, "Y": -3, "Z": 4}, "expected": -24},
        ]

        correct = 0
        total = len(test_cases)

        for case in test_cases:
            try:
                req = evaluator_pb2.EvalRequest(expr=case["expr"], data=case["data"])
                resp = stub.Evaluate(req, timeout=2.0)
                if resp.result == case["expected"]:
                    correct += 1
            except Exception as e:
                pass # Ignore errors, they will just result in a lower accuracy score

        accuracy = correct / total
        assert accuracy >= 1.0, f"Accuracy metric failed: {accuracy} < 1.0"