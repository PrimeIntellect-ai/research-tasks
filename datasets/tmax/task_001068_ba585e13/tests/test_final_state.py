# test_final_state.py

import os
import subprocess
import pytest
import requests

def get_expected_score(frame_num):
    cmd = [
        "ffmpeg", "-i", "/app/test_sequence.mp4",
        "-vf", f"select=eq(n\\,{frame_num})",
        "-vframes", "1",
        "-pix_fmt", "gray",
        "-f", "image2pipe",
        "-vcodec", "rawvideo",
        "-"
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if result.returncode != 0 or not result.stdout:
        pytest.fail(f"Failed to extract frame {frame_num} using ffmpeg")

    data = result.stdout
    sum_val = sum(data)
    max_val = max(data) if data else 0

    if max_val == 255:
        return -1
    return sum_val // (255 - max_val)

@pytest.mark.parametrize("frame", [0, 10, 42])
def test_score_endpoint(frame):
    expected = get_expected_score(frame)
    url = f"http://127.0.0.1:9000/score?frame={frame}"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to service for frame {frame} at {url}: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 OK for frame {frame}, got {resp.status_code}"
    assert resp.text.strip() == str(expected), f"Expected score {expected} for frame {frame}, got '{resp.text.strip()}'"