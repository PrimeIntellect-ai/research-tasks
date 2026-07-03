# test_final_state.py

import os
import glob
import socket
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_truth_frames():
    """Generate ground truth frames using ffmpeg."""
    truth_dir = "/tmp/truth_frames"
    os.makedirs(truth_dir, exist_ok=True)

    # Run ffmpeg to extract frames
    cmd = [
        "ffmpeg", "-y", "-i", "/app/cctv.mp4", 
        "-r", "1", "-vframes", "30", 
        "-f", "image2", "-vcodec", "pgm", 
        f"{truth_dir}/truth_frame_%03d.pgm"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    yield truth_dir

def test_spool_directory_empty():
    """Check that /home/user/spool/ exists and is empty."""
    spool_dir = "/home/user/spool"
    assert os.path.isdir(spool_dir), f"Directory {spool_dir} does not exist."

    # Check if empty
    files = os.listdir(spool_dir)
    assert len(files) == 0, f"Directory {spool_dir} is not empty. Found: {files}"

def test_archive_file_exists_and_compressed(setup_truth_frames):
    """Check that video_archive.bin exists and is smaller than the sum of raw frames."""
    archive_path = "/home/user/video_archive.bin"
    assert os.path.isfile(archive_path), f"Archive file {archive_path} does not exist."

    archive_size = os.path.getsize(archive_path)

    # Calculate sum of truth frame sizes
    truth_dir = setup_truth_frames
    truth_files = glob.glob(f"{truth_dir}/truth_frame_*.pgm")
    assert len(truth_files) > 0, "No truth frames were generated."

    total_raw_size = sum(os.path.getsize(f) for f in truth_files)

    # Assert archive is at least 10% smaller
    assert archive_size <= total_raw_size * 0.9, (
        f"Archive size ({archive_size} bytes) is not at least 10% smaller than "
        f"total raw size ({total_raw_size} bytes)."
    )

def fetch_frame(filename):
    """Helper to fetch a frame from the TCP service."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect(("127.0.0.1", 8888))
        request = f"FETCH {filename}\n".encode("utf-8")
        s.sendall(request)

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    return response

def test_tcp_fetch_frame_007(setup_truth_frames):
    """Test fetching frame_007.pgm over TCP."""
    response = fetch_frame("frame_007.pgm")

    truth_file = f"{setup_truth_frames}/truth_frame_007.pgm"
    with open(truth_file, "rb") as f:
        truth_data = f.read()

    assert response == truth_data, "Fetched frame_007.pgm does not match ground truth byte-for-byte."

def test_tcp_fetch_frame_029(setup_truth_frames):
    """Test fetching frame_029.pgm over TCP."""
    response = fetch_frame("frame_029.pgm")

    truth_file = f"{setup_truth_frames}/truth_frame_029.pgm"
    with open(truth_file, "rb") as f:
        truth_data = f.read()

    assert response == truth_data, "Fetched frame_029.pgm does not match ground truth byte-for-byte."

def test_tcp_fetch_missing_frame():
    """Test fetching a non-existent frame over TCP."""
    response = fetch_frame("frame_999.pgm")
    assert response == b"ERROR\n", f"Expected 'ERROR\\n' for missing frame, got {response!r}"