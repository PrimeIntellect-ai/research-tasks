# test_final_state.py

import os
import time
import subprocess
import pytest
import pandas as pd
import numpy as np
import imageio.v3 as iio

def get_expected_event_ids():
    # 1. Extract expected intensities from the video
    # imageio reads as RGB. cv2.cvtColor with COLOR_BGR2GRAY uses:
    # Y = 0.299 R + 0.587 G + 0.114 B
    # Since the original was written as BGR, imageio's R is cv2's R.
    video_path = '/app/experiment.mp4'
    frames = iio.imread(video_path)

    expected_intensities = set()
    for frame in frames:
        # frame is RGB
        gray = 0.299 * frame[:,:,0] + 0.587 * frame[:,:,1] + 0.114 * frame[:,:,2]
        expected_intensities.add(int(np.round(gray.mean())))

    # 2. Read the history dataset
    df = pd.read_csv('/app/history.csv')

    # 3. Filter based on conditions
    filtered = df[
        (df['intensity'].isin(expected_intensities)) & 
        (df['category'].isin(['A', 'C']))
    ]

    # 4. Sort by timestamp desc, then event_id asc
    filtered = filtered.sort_values(by=['timestamp', 'event_id'], ascending=[False, True])

    # 5. Paginate: 2nd page, size 50 (skip 50, take 50)
    page_2 = filtered.iloc[50:100]

    return page_2['event_id'].astype(str).tolist()

def test_fast_query_accuracy_and_performance():
    script_path = '/home/user/fast_query.py'
    assert os.path.exists(script_path), f"Script not found at {script_path}"

    # Run the script and measure time
    start_time = time.time()
    result = subprocess.run(
        ['python3', script_path], 
        capture_output=True, 
        text=True
    )
    end_time = time.time()
    execution_time = end_time - start_time

    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    # Parse output
    output_ids = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    expected_ids = get_expected_event_ids()

    # Check accuracy
    assert output_ids == expected_ids, (
        f"Output event_ids do not match expected.\n"
        f"Expected first 5: {expected_ids[:5]}\n"
        f"Got first 5: {output_ids[:5]}"
    )

    # Check performance metric
    threshold = 0.25
    assert execution_time <= threshold, (
        f"Performance failed: execution time was {execution_time:.4f} seconds, "
        f"which exceeds the threshold of {threshold} seconds. "
        f"Did you forget to create an index in the SQLite database?"
    )

def test_database_and_frames_exist():
    db_path = '/home/user/data.db'
    frames_path = '/home/user/frames.csv'

    assert os.path.exists(frames_path), f"Frames CSV not found at {frames_path}"
    assert os.path.exists(db_path), f"SQLite database not found at {db_path}"
    assert os.path.getsize(db_path) > 0, "SQLite database is empty"