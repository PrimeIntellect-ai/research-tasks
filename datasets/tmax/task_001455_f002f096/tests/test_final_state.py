# test_final_state.py
import os
import json
import requests
import glob

def test_frames_extracted():
    """Test that frames were extracted to /home/user/frames/."""
    frames_dir = "/home/user/frames"
    assert os.path.exists(frames_dir), f"Directory does not exist: {frames_dir}"
    frames = glob.glob(os.path.join(frames_dir, "frame_*.jpg"))
    assert len(frames) > 0, "No frames were extracted to /home/user/frames/"

def test_embeddings_json():
    """Test the structure and mathematical constraints of embeddings.json."""
    json_path = "/home/user/embeddings.json"
    assert os.path.exists(json_path), f"File does not exist: {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "embeddings.json is not valid JSON"

    assert len(data) > 0, "embeddings.json is empty"
    for k, v in data.items():
        assert isinstance(v, list), f"Embedding for frame {k} is not a list"
        assert len(v) == 8, f"Embedding for frame {k} does not have exactly 8 elements"
        assert all(isinstance(x, (int, float)) for x in v), f"Embedding for frame {k} contains non-numeric values"
        assert abs(sum(v) - 1.0) < 0.005, f"Embedding for frame {k} does not sum to 1.0 (sum is {sum(v)})"

def test_api_tokenize():
    """Test the /api/tokenize endpoint."""
    url = "http://127.0.0.1:8888/api/tokenize"
    payload = {"text": "Hello, World! 123"}
    try:
        resp = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to {url}: {e}"

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        assert False, "Response from /api/tokenize is not valid JSON"

    assert "tokens" in data, "Response JSON missing 'tokens' key"
    expected_tokens = ["hello", "world", "123"]
    assert data["tokens"] == expected_tokens, f"Expected tokens {expected_tokens}, got {data['tokens']}"

def test_api_embedding():
    """Test the /api/embedding endpoint."""
    url = "http://127.0.0.1:8888/api/embedding?id=1"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to {url}: {e}"

    assert resp.status_code == 200, f"Expected HTTP 200 for id=1 (video is >3s long), got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        assert False, "Response from /api/embedding is not valid JSON"

    assert "id" in data, "Response JSON missing 'id' key"
    assert data["id"] == 1, f"Expected id to be 1, got {data['id']}"

    assert "embedding" in data, "Response JSON missing 'embedding' key"
    embedding = data["embedding"]
    assert isinstance(embedding, list), "Embedding must be a list"
    assert len(embedding) == 8, "Embedding must have exactly 8 elements"
    assert abs(sum(embedding) - 1.0) < 0.005, f"Embedding must sum to 1.0 (sum is {sum(embedding)})"