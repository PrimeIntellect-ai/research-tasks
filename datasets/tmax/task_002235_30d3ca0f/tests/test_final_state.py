# test_final_state.py
import os

def test_results_log_exists():
    assert os.path.exists("/home/user/results.log"), "/home/user/results.log does not exist"

def test_results_log_content():
    expected_content = """1_linear.asm: 8.00
2_forward.asm: 13.00
3_loop.asm: 19.50"""

    with open("/home/user/results.log", "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Expected results.log to contain:\n{expected_content}\nBut got:\n{actual_content}"

def test_proto_file_exists():
    assert os.path.exists("/home/user/analyzer.proto"), "/home/user/analyzer.proto does not exist"

def test_server_file_exists():
    assert os.path.exists("/home/user/server.py"), "/home/user/server.py does not exist"

def test_client_file_exists():
    assert os.path.exists("/home/user/client.py"), "/home/user/client.py does not exist"

def test_generated_pb2_files_exist():
    assert os.path.exists("/home/user/analyzer_pb2.py"), "analyzer_pb2.py was not generated"
    assert os.path.exists("/home/user/analyzer_pb2_grpc.py"), "analyzer_pb2_grpc.py was not generated"