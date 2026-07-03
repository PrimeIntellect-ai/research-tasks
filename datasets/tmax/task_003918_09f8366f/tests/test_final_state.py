# test_final_state.py

import os
import sqlite3
import subprocess
import tempfile
import numpy as np
import pytest

def test_frames_extracted():
    frames_dir = '/home/user/frames'
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} is missing."
    frames = [f for f in os.listdir(frames_dir) if f.endswith('.pgm')]
    assert len(frames) > 0, "No PGM frames found in /home/user/frames."

def test_db_schema_updated():
    db_path = '/home/user/analytics.db'
    assert os.path.isfile(db_path), f"{db_path} missing."

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(frame_stats);")
    columns = {row[1]: row[2].upper() for row in cur.fetchall()}

    assert 'diff_score' in columns, "Column 'diff_score' missing in frame_stats."
    assert 'timestamp_ms' in columns, "Column 'timestamp_ms' missing in frame_stats."
    conn.close()

def compute_ground_truth_mad():
    video_path = '/app/video.mp4'
    assert os.path.isfile(video_path), "Reference video missing."

    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract frames using ffmpeg exactly as specified
        cmd = [
            'ffmpeg', '-i', video_path,
            '-r', '10',
            '-pix_fmt', 'gray',
            os.path.join(tmpdir, '%04d.pgm')
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        frames = sorted([f for f in os.listdir(tmpdir) if f.endswith('.pgm')])

        mad_values = {}
        prev_img = None
        for i, frame_file in enumerate(frames):
            frame_num = i + 1
            # Read PGM
            with open(os.path.join(tmpdir, frame_file), 'rb') as f:
                header = f.readline()
                # Skip comments
                while True:
                    line = f.readline()
                    if not line.startswith(b'#'):
                        break
                dims = line.split()
                width, height = int(dims[0]), int(dims[1])
                maxval = int(f.readline())
                data = f.read()
                img = np.frombuffer(data, dtype=np.uint8).astype(np.float32)

            if prev_img is not None:
                mad = np.mean(np.abs(img - prev_img))
                mad_values[frame_num] = mad
            prev_img = img

    return mad_values

def test_db_contents_and_mse():
    db_path = '/home/user/analytics.db'
    assert os.path.isfile(db_path), f"{db_path} missing."

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT frame_num, diff_score, timestamp_ms FROM frame_stats ORDER BY frame_num")
    agent_data = cur.fetchall()
    conn.close()

    assert len(agent_data) > 0, "No data found in frame_stats."

    gt_mad = compute_ground_truth_mad()
    assert len(agent_data) == len(gt_mad), f"Expected {len(gt_mad)} rows in DB, got {len(agent_data)}."

    mse_list = []
    for row in agent_data:
        frame_num, diff_score, timestamp_ms = row
        assert frame_num in gt_mad, f"Unexpected frame_num {frame_num} in DB."

        expected_timestamp = (frame_num - 1) * 100
        assert timestamp_ms == expected_timestamp, f"Expected timestamp_ms {expected_timestamp} for frame {frame_num}, got {timestamp_ms}."

        expected_mad = gt_mad[frame_num]
        mse_list.append((diff_score - expected_mad)**2)

    mse = np.mean(mse_list)
    assert mse <= 0.05, f"MSE of diff_score is {mse:.4f}, which is > 0.05 threshold."