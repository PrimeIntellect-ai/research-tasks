# test_final_state.py
import os
import time
import subprocess
import pytest

def test_speedup_and_correctness():
    video_path = "/app/test_video.mp4"
    assert os.path.exists(video_path), f"Test video {video_path} is missing."

    # Run reference.py
    start_ref = time.time()
    subprocess.run(["python3", "/home/user/reference.py"], check=True)
    end_ref = time.time()
    ref_time = end_ref - start_ref

    assert os.path.exists('/home/user/output_indices.txt'), "reference.py did not produce /home/user/output_indices.txt"
    with open('/home/user/output_indices.txt', 'r') as f:
        ref_indices = f.read().splitlines()

    # Remove the file to ensure fast_pipeline.py actually creates it
    os.remove('/home/user/output_indices.txt')

    # Run fast_pipeline.py
    start_fast = time.time()
    subprocess.run(["python3", "/home/user/fast_pipeline.py"], check=True)
    end_fast = time.time()
    fast_time = end_fast - start_fast

    assert os.path.exists('/home/user/output_indices.txt'), "fast_pipeline.py did not produce /home/user/output_indices.txt"
    with open('/home/user/output_indices.txt', 'r') as f:
        fast_indices = f.read().splitlines()

    assert len(ref_indices) == 50, f"Expected 50 indices from reference, got {len(ref_indices)}"
    assert ref_indices == fast_indices, "The output indices of fast_pipeline.py do not match reference.py exactly."

    speedup = ref_time / fast_time
    assert speedup >= 2.5, f"Speedup is {speedup:.2f}x, which is less than the required 2.5x threshold. (Ref time: {ref_time:.2f}s, Fast time: {fast_time:.2f}s)"