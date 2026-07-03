# test_final_state.py
import os
import subprocess

def test_build_and_test_script_execution():
    script_path = "/home/user/compat/build_and_test.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Execute the script to ensure it runs flawlessly
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"Script failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )

def test_integration_log_contents():
    log_path = "/home/user/compat/integration.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["True", "False", "True"]
    assert lines == expected, f"Expected log contents to be {expected}, but got {lines}."

def test_generated_protos_exist():
    pb2_path = "/home/user/compat/server/compat_pb2.py"
    pb2_grpc_path = "/home/user/compat/server/compat_pb2_grpc.py"

    assert os.path.exists(pb2_path), f"Generated protobuf file {pb2_path} does not exist."
    assert os.path.exists(pb2_grpc_path), f"Generated gRPC file {pb2_grpc_path} does not exist."

def test_semver_tests_pass():
    test_file = "/home/user/compat/tests/test_semver.py"
    assert os.path.exists(test_file), f"Test file {test_file} does not exist."

    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"pytest failed for {test_file}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )

def test_proto_file_exists():
    proto_path = "/home/user/compat/proto/compat.proto"
    assert os.path.exists(proto_path), f"Protobuf definition {proto_path} does not exist."

def test_python_source_files_exist():
    semver_path = "/home/user/compat/server/semver.py"
    main_path = "/home/user/compat/server/main.py"

    assert os.path.exists(semver_path), f"Source file {semver_path} does not exist."
    assert os.path.exists(main_path), f"Source file {main_path} does not exist."