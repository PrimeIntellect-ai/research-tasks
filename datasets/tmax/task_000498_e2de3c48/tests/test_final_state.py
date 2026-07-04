# test_final_state.py

import os
import time
import subprocess
import pandas as pd
import pytest

def test_merged_results_valid():
    csv_path = '/home/user/merged_results.csv'
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    df = pd.read_csv(csv_path)
    expected_columns = ['timestamp', 'object_count', 'speed', 'lat', 'lon']
    assert list(df.columns) == expected_columns, f"Columns mismatch. Expected {expected_columns}, got {list(df.columns)}"
    assert len(df) > 0, "The merged_results.csv dataframe is empty."

def test_optimized_pipeline_speedup():
    agent_script = '/home/user/optimized_pipeline.py'
    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."

    # Create a 10-second dummy video for testing
    test_video = '/tmp/test_video.mp4'
    if os.path.exists(test_video):
        os.remove(test_video)

    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc=duration=10:size=640x480:rate=30',
        '-c:v', 'libx264', test_video
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    test_out_csv = '/tmp/test_out.csv'
    if os.path.exists(test_out_csv):
        os.remove(test_out_csv)

    # Benchmark agent's script
    t0 = time.time()
    try:
        subprocess.run(['python3', agent_script, test_video, test_out_csv], check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script failed to run on test video: {e}")
    agent_time = time.time() - t0

    assert os.path.isfile(test_out_csv), "Agent script did not produce the output CSV on the test video."

    # Benchmark sequential baseline
    t_seq_0 = time.time()
    subprocess.run(['ffmpeg', '-y', '-i', test_video, '-vf', 'fps=1', '/tmp/test_frames_%04d.png'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    frames = [f for f in os.listdir('/tmp') if f.startswith('test_frames_') and f.endswith('.png')]
    for f in frames:
        subprocess.run(['python3', '/app/baseline_inference.py', f'/tmp/{f}'], check=True, stdout=subprocess.DEVNULL)

    seq_time = time.time() - t_seq_0

    speedup = seq_time / agent_time
    assert speedup >= 2.0, f"Pipeline speedup is {speedup:.2f}x, which is below the required 2.0x threshold. (Agent time: {agent_time:.2f}s, Sequential baseline time: {seq_time:.2f}s)"