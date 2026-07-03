# test_final_state.py
import os
import socket
import pytest

FRAMES_DIR = "/home/user/frames"
CSV_PATH = "/home/user/etl/embeddings.csv"
HOST = "127.0.0.1"
PORT = 9090

def compute_expected_embedding(raw_bytes):
    cells = [0.0] * 16
    for y in range(240):
        for x in range(320):
            idx = (y * 320 + x) * 3
            r = raw_bytes[idx]
            g = raw_bytes[idx+1]
            b = raw_bytes[idx+2]
            gray = 0.299 * r + 0.587 * g + 0.114 * b
            cell_x = x // 80
            cell_y = y // 60
            cell_idx = cell_y * 4 + cell_x
            cells[cell_idx] += gray
    for i in range(16):
        cells[i] /= (80 * 60)
    return cells

def test_frames_extracted():
    assert os.path.exists(FRAMES_DIR), f"Directory {FRAMES_DIR} does not exist."
    for i in range(1, 11):
        frame_name = f"frame_{i:02d}.raw"
        frame_path = os.path.join(FRAMES_DIR, frame_name)
        assert os.path.exists(frame_path), f"Frame {frame_name} missing."
        assert os.path.getsize(frame_path) == 230400, f"Frame {frame_name} has incorrect size."

def test_embeddings_csv():
    assert os.path.exists(CSV_PATH), f"CSV file {CSV_PATH} missing."
    frame_01_path = os.path.join(FRAMES_DIR, "frame_01.raw")
    with open(frame_01_path, "rb") as f:
        raw_bytes = f.read()

    expected_emb = compute_expected_embedding(raw_bytes)

    with open(CSV_PATH, "r") as f:
        lines = f.read().strip().split("\n")

    frame_01_line = None
    for line in lines:
        if line.startswith("frame_01.raw"):
            frame_01_line = line
            break

    assert frame_01_line is not None, "frame_01.raw not found in embeddings.csv"
    parts = frame_01_line.split(",")
    assert len(parts) == 17, "embeddings.csv line should have 17 columns (filename + 16 values)"

    for i in range(16):
        actual_val = float(parts[i+1])
        expected_val = expected_emb[i]
        assert abs(actual_val - expected_val) <= 0.05, f"Embedding value {i} mismatch for frame_01.raw: expected ~{expected_val:.2f}, got {actual_val}"

def test_tcp_server():
    frame_03_path = os.path.join(FRAMES_DIR, "frame_03.raw")
    assert os.path.exists(frame_03_path), "frame_03.raw missing, cannot test server properly."

    with open(frame_03_path, "rb") as f:
        raw_bytes = f.read()

    expected_emb = compute_expected_embedding(raw_bytes)
    query_str = "SEARCH " + ",".join(f"{v:.2f}" for v in expected_emb) + "\n"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        pytest.fail(f"Failed to connect to TCP server at {HOST}:{PORT}: {e}")

    try:
        s.sendall(query_str.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        assert response == "MATCH frame_03.raw\n", f"Expected 'MATCH frame_03.raw\\n', got {repr(response)}"

        s.sendall(b"QUIT\n")
        # Ensure connection is closed
        resp = s.recv(1024)
        assert resp == b"", "Connection should be closed after QUIT"
    finally:
        s.close()