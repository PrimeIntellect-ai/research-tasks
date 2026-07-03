# test_final_state.py

import os
import sys
import stat
import tempfile
import importlib.util
import pytest

try:
    import grpc
    from grpc_tools import protoc
except ImportError:
    pytest.fail("grpcio or grpcio-tools is not installed.")

try:
    import cv2
except ImportError:
    pytest.fail("opencv-python (cv2) is not installed.")

PIPELINE_DIR = "/home/user/video_pipeline"
BUILD_SH = os.path.join(PIPELINE_DIR, "build.sh")
LIB_SO = os.path.join(PIPELINE_DIR, "libchecksum.so")
PROTO_FILE = os.path.join(PIPELINE_DIR, "service.proto")
VIDEO_FILE = "/app/drone_flight.mp4"

def compute_expected_checksum(frame_number: int) -> int:
    cap = cv2.VideoCapture(VIDEO_FILE)
    if not cap.isOpened():
        pytest.fail(f"Could not open video file {VIDEO_FILE}")

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        pytest.fail(f"Could not read frame {frame_number} from {VIDEO_FILE}")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    data = gray.flatten().tobytes()

    checksum = 0x811c9dc5
    for byte in data:
        checksum ^= byte
        checksum = (checksum * 0x01000193) & 0xFFFFFFFF

    return checksum

def test_build_script_exists_and_executable():
    assert os.path.exists(BUILD_SH), f"Build script {BUILD_SH} does not exist."
    st = os.stat(BUILD_SH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Build script {BUILD_SH} is not executable."

def test_libchecksum_exists():
    assert os.path.exists(LIB_SO), f"Shared library {LIB_SO} does not exist."

def test_grpc_service():
    assert os.path.exists(PROTO_FILE), f"Proto file {PROTO_FILE} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        # Compile proto
        protoc_args = [
            'grpc_tools.protoc',
            f'--proto_path={PIPELINE_DIR}',
            f'--python_out={tmpdir}',
            f'--grpc_python_out={tmpdir}',
            PROTO_FILE
        ]
        if protoc.main(protoc_args) != 0:
            pytest.fail("Failed to compile service.proto")

        sys.path.insert(0, tmpdir)
        try:
            import service_pb2
            import service_pb2_grpc
        except ImportError as e:
            pytest.fail(f"Failed to import generated proto modules: {e}")

        frame_number = 15
        expected_checksum = compute_expected_checksum(frame_number)

        try:
            channel = grpc.insecure_channel('0.0.0.0:50051')
            stub = service_pb2_grpc.FrameAnalyzerStub(channel)
            request = service_pb2.FrameRequest(frame_number=frame_number)
            response = stub.GetFrameChecksum(request, timeout=5)

            assert response.checksum == expected_checksum, f"Expected checksum {expected_checksum}, but got {response.checksum}"
        except grpc.RpcError as e:
            pytest.fail(f"gRPC call failed: {e}")
        finally:
            sys.path.pop(0)