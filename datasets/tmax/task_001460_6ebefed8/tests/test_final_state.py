# test_final_state.py

import os
import subprocess
import numpy as np
import pytest
from PIL import Image

def compute_reference():
    os.makedirs('/tmp/ref_frames', exist_ok=True)
    subprocess.run([
        'ffmpeg', '-y', '-i', '/app/experiment_feed.mp4', '-vf', 'fps=4,scale=128:128,format=gray',
        '/tmp/ref_frames/frame_%04d.png'
    ], check=True, capture_output=True)

    frames = []
    for file in sorted(os.listdir('/tmp/ref_frames')):
        if file.endswith('.png'):
            img = Image.open(os.path.join('/tmp/ref_frames', file))
            frames.append(np.array(img))
    return np.array(frames)

def test_dataset_npz_and_metric():
    dataset_path = '/home/user/dataset.npz'
    assert os.path.exists(dataset_path), f"File {dataset_path} does not exist."

    try:
        data = np.load(dataset_path)
        agent_frames = data['frames']
    except Exception as e:
        pytest.fail(f"Could not load 'frames' from {dataset_path}: {e}")

    assert agent_frames.dtype == np.uint8, f"Expected dtype uint8, got {agent_frames.dtype}"

    ref_frames = compute_reference()
    assert agent_frames.shape == ref_frames.shape, f"Shape mismatch: expected {ref_frames.shape}, got {agent_frames.shape}"

    mse = np.mean((agent_frames.astype(np.float32) - ref_frames.astype(np.float32)) ** 2)
    assert mse <= 2.0, f"MSE {mse} is greater than the threshold 2.0"

def test_chunks():
    dataset_path = '/home/user/dataset.npz'
    assert os.path.exists(dataset_path)
    agent_frames = np.load(dataset_path)['frames']

    chunks_dir = '/home/user/chunks'
    assert os.path.exists(chunks_dir) and os.path.isdir(chunks_dir), f"Directory {chunks_dir} does not exist."

    num_frames = len(agent_frames)
    expected_num_chunks = (num_frames + 49) // 50

    chunk_files = sorted([f for f in os.listdir(chunks_dir) if f.endswith('.npz')])
    assert len(chunk_files) == expected_num_chunks, f"Expected {expected_num_chunks} chunks, got {len(chunk_files)}"

    for i in range(expected_num_chunks):
        expected_filename = f"chunk_{i:03d}.npz"
        assert expected_filename in chunk_files, f"Expected chunk file {expected_filename} not found."

        chunk_path = os.path.join(chunks_dir, expected_filename)
        try:
            chunk_data = np.load(chunk_path)['frames']
        except Exception as e:
            pytest.fail(f"Could not load 'frames' from {chunk_path}: {e}")

        start_idx = i * 50
        end_idx = min((i + 1) * 50, num_frames)
        expected_chunk = agent_frames[start_idx:end_idx]

        assert np.array_equal(chunk_data, expected_chunk), f"Data mismatch in {expected_filename}"

def test_watcher_script():
    watcher_path = '/home/user/watcher.py'
    assert os.path.exists(watcher_path), f"File {watcher_path} does not exist."

    with open(watcher_path, 'r') as f:
        content = f.read()

    assert 'watchdog' in content, "The watcher script does not seem to use the 'watchdog' library."
    assert '/home/user/incoming' in content or '/home/user/incoming/' in content, "The watcher script does not contain the incoming directory path."
    assert '/home/user/processed' in content or '/home/user/processed/' in content, "The watcher script does not contain the processed directory path."