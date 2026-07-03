# test_final_state.py
import os
import sys
import math
import pytest

def test_files_exist():
    assert os.path.isfile("/home/user/app/video.proto"), "video.proto is missing"
    assert os.path.isfile("/home/user/app/server.py"), "server.py is missing"
    assert os.path.isfile("/home/user/app/ci_setup.sh"), "ci_setup.sh is missing"
    assert os.access("/home/user/app/ci_setup.sh", os.X_OK), "ci_setup.sh is not executable"
    assert os.path.isfile("/home/user/app/server.pid"), "server.pid is missing, server might not be running"

def test_grpc_service():
    # Ensure the student's compiled protobuf files are in the path
    sys.path.insert(0, '/home/user/app')
    try:
        import video_pb2
        import video_pb2_grpc
        import grpc
        import cv2
        import numpy as np
    except ImportError as e:
        pytest.fail(f"Failed to import required modules. Did ci_setup.sh install them and compile the proto? Error: {e}")

    # Ground truth computation
    video_path = '/app/sample.mp4'
    assert os.path.isfile(video_path), "Sample video is missing from /app/sample.mp4"

    cap = cv2.VideoCapture(video_path)
    assert cap.isOpened(), "Failed to open /app/sample.mp4"

    variances = []
    for i in range(21):
        ret, frame = cap.read()
        if not ret:
            break
        if i >= 10:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            variances.append(np.var(gray))

    cap.release()
    assert len(variances) > 0, "Could not read frames 10 to 20 from video"
    expected_variance = np.mean(variances)

    # gRPC request
    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = video_pb2_grpc.VideoProcessorStub(channel)
        request = video_pb2.FrameRangeRequest(start_frame=10, end_frame=20)
        response = stub.AnalyzeFrameRange(request, timeout=10)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e}")

    actual_variance = response.average_variance

    assert abs(actual_variance - expected_variance) < 0.1, \
        f"Expected average variance ~{expected_variance:.3f}, but got {actual_variance:.3f}"