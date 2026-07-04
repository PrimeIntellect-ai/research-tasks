# test_final_state.py

import os
import socket
import requests
import pytest

def test_symlinks_cleaned():
    assert not os.path.lexists("/home/user/dataset/loop1"), "/home/user/dataset/loop1 should have been deleted"
    assert not os.path.lexists("/home/user/dataset/loop2"), "/home/user/dataset/loop2 should have been deleted"
    assert not os.path.lexists("/home/user/dataset/broken_link"), "/home/user/dataset/broken_link should have been deleted"

def test_archives_moved():
    assert not os.path.exists("/home/user/dataset/archives/bad_data.zip"), "bad_data.zip should not be in archives directory"
    assert os.path.exists("/home/user/dataset/corrupt/bad_data.zip"), "bad_data.zip should be moved to corrupt directory"

def test_files_renamed_and_modified():
    file_101 = "/home/user/dataset/extracted/processed_101.txt"
    file_202 = "/home/user/dataset/extracted/processed_202.txt"

    assert os.path.exists(file_101), f"{file_101} does not exist"
    assert os.path.exists(file_202), f"{file_202} does not exist"

    with open(file_101, "r") as f:
        content_101 = f.read()
        assert "VERIFIED" in content_101, f"VERIFIED not appended to {file_101}"

    with open(file_202, "r") as f:
        content_202 = f.read()
        assert "VERIFIED" in content_202, f"VERIFIED not appended to {file_202}"

def test_video_frame_extracted():
    assert os.path.exists("/home/user/dataset/video_frame.jpg"), "video_frame.jpg was not extracted"
    assert os.path.getsize("/home/user/dataset/video_frame.jpg") > 0, "video_frame.jpg is empty"

def test_http_service():
    try:
        resp_txt = requests.get("http://127.0.0.1:8080/extracted/processed_101.txt", timeout=5)
        assert resp_txt.status_code == 200, f"HTTP GET /extracted/processed_101.txt returned {resp_txt.status_code}"
        assert "VERIFIED" in resp_txt.text, "HTTP response for processed_101.txt does not contain VERIFIED"

        resp_img = requests.get("http://127.0.0.1:8080/video_frame.jpg", timeout=5)
        assert resp_img.status_code == 200, f"HTTP GET /video_frame.jpg returned {resp_img.status_code}"
        assert len(resp_img.content) > 0, "HTTP response for video_frame.jpg is empty"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP service check failed: {e}")

def test_tcp_service():
    frame_path = "/home/user/dataset/video_frame.jpg"
    assert os.path.exists(frame_path), "video_frame.jpg must exist to test TCP service"
    expected_size = os.path.getsize(frame_path)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(("127.0.0.1", 8081))
        s.sendall(b"GET_FRAME_SIZE\n")

        response = s.recv(1024).decode("utf-8")
        s.close()

        assert response.strip() == str(expected_size), f"TCP service returned '{response.strip()}', expected '{expected_size}'"
        assert response.endswith("\n"), "TCP service response must end with a newline"
    except Exception as e:
        pytest.fail(f"TCP service check failed: {e}")