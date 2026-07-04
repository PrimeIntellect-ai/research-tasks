# test_final_state.py
import os
import stat
import subprocess
import sys
import time
import shutil
import pytest

DIR_SYNC_PATH = "/home/user/dir_sync"
PROTO_FILE = os.path.join(DIR_SYNC_PATH, "sync.proto")
E2E_SCRIPT = os.path.join(DIR_SYNC_PATH, "run_e2e.sh")
SERVER_FILE = os.path.join(DIR_SYNC_PATH, "server.py")
CLIENT_FILE = os.path.join(DIR_SYNC_PATH, "client.py")

def test_files_exist():
    """Check if the required files exist."""
    assert os.path.isdir(DIR_SYNC_PATH), f"{DIR_SYNC_PATH} does not exist"
    assert os.path.isfile(PROTO_FILE), f"{PROTO_FILE} does not exist"
    assert os.path.isfile(E2E_SCRIPT), f"{E2E_SCRIPT} does not exist"
    assert os.path.isfile(SERVER_FILE), f"{SERVER_FILE} does not exist"
    assert os.path.isfile(CLIENT_FILE), f"{CLIENT_FILE} does not exist"

def test_e2e_script_executable_and_passes():
    """Check if run_e2e.sh is executable and outputs E2E TEST PASSED."""
    st = os.stat(E2E_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{E2E_SCRIPT} is not executable"

    # Run the e2e script
    result = subprocess.run(
        ["bash", E2E_SCRIPT],
        cwd=DIR_SYNC_PATH,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"run_e2e.sh failed with code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert "E2E TEST PASSED" in result.stdout, "run_e2e.sh did not output 'E2E TEST PASSED'"

def test_grpc_server_functionality():
    """Test the CalculateDiff and ApplyPatch RPC methods."""
    sys.path.insert(0, DIR_SYNC_PATH)

    # Ensure pb2 files are generated (they should be after run_e2e.sh, but just in case)
    subprocess.run([
        sys.executable, "-m", "grpc_tools.protoc",
        f"-I{DIR_SYNC_PATH}",
        f"--python_out={DIR_SYNC_PATH}",
        f"--grpc_python_out={DIR_SYNC_PATH}",
        PROTO_FILE
    ], check=True)

    try:
        import sync_pb2
        import sync_pb2_grpc
        import grpc
    except ImportError as e:
        pytest.fail(f"Failed to import generated protobuf modules: {e}")

    # Start the server
    server_process = subprocess.Popen(
        [sys.executable, SERVER_FILE],
        cwd=DIR_SYNC_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(2) # Wait for server to start

    if server_process.poll() is not None:
        stdout, stderr = server_process.communicate()
        pytest.fail(f"Server failed to start. Stdout: {stdout}, Stderr: {stderr}")

    source_dir = "/tmp/grpc_test_source"
    target_dir = "/tmp/grpc_test_target"

    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    os.makedirs(source_dir)
    os.makedirs(target_dir)

    # Create differing files
    with open(os.path.join(source_dir, "file1.txt"), "w") as f:
        f.write("Hello World\nLine 2\n")

    with open(os.path.join(target_dir, "file1.txt"), "w") as f:
        f.write("Hello World\nLine 2 Modified\n")

    with open(os.path.join(target_dir, "file2.txt"), "w") as f:
        f.write("New file\n")

    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = sync_pb2_grpc.DirSyncStub(channel)

        # Calculate diff from source to target
        diff_req = sync_pb2.DiffRequest(source_dir=source_dir, target_dir=target_dir)
        diff_resp = stub.CalculateDiff(diff_req)

        assert len(diff_resp.patch_lines) > 0, "Expected patch lines but got none"

        # Apply patch to source directory so it matches target
        patch_req = sync_pb2.PatchRequest(target_dir=source_dir, patch_lines=diff_resp.patch_lines)
        patch_resp = stub.ApplyPatch(patch_req)

        assert patch_resp.success is True, "ApplyPatch returned success=False"

        # Verify directories are identical
        diff_result = subprocess.run(
            ["diff", "-r", source_dir, target_dir],
            capture_output=True,
            text=True
        )
        assert diff_result.returncode == 0, f"Directories do not match after patch: {diff_result.stdout}"

    finally:
        server_process.terminate()
        server_process.wait()
        shutil.rmtree(source_dir, ignore_errors=True)
        shutil.rmtree(target_dir, ignore_errors=True)