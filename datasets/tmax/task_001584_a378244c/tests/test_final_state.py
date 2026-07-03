# test_final_state.py
import os
import json
import subprocess
import numpy as np
from scipy import stats
import imageio.v3 as iio
import pytest

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"Results file missing at {results_path}"

    with open(results_path, "r") as f:
        try:
            agent_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    # Required keys
    required_keys = [
        "most_similar_frame_file",
        "min_l2_distance",
        "brightness_mean",
        "brightness_ci_lower",
        "brightness_ci_upper"
    ]
    for k in required_keys:
        assert k in agent_results, f"Key '{k}' missing from results.json"

    # Compute ground truth
    truth_frames_dir = "/tmp/truth_frames"
    os.makedirs(truth_frames_dir, exist_ok=True)

    # Extract frames as PNG to avoid JPEG compression differences
    subprocess.run(["ffmpeg", "-y", "-i", "/app/video.mp4", "-vf", "fps=1", os.path.join(truth_frames_dir, "frame_%04d.png")], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    frames = sorted(os.listdir(truth_frames_dir))
    assert len(frames) > 1, "Not enough frames extracted from video to perform analysis"

    embeddings = []
    brightnesses = []

    for f in frames:
        img = iio.imread(os.path.join(truth_frames_dir, f))
        avg_color = img.mean(axis=(0, 1))[:3]  # Ensure RGB
        embeddings.append(avg_color)
        brightnesses.append(avg_color.mean())

    embeddings = np.array(embeddings)
    brightnesses = np.array(brightnesses)

    # Similar frame
    ref = embeddings[0]
    dists = np.linalg.norm(embeddings[1:] - ref, axis=1)
    best_idx = np.argmin(dists) + 1
    min_dist = dists[best_idx - 1]
    best_frame_png = frames[best_idx]
    best_frame_jpg = best_frame_png.replace(".png", ".jpg")

    # Confidence Interval
    mean_b = np.mean(brightnesses)
    sem_b = stats.sem(brightnesses)
    ci = stats.t.interval(0.95, len(brightnesses) - 1, loc=mean_b, scale=sem_b)

    # Validate agent results
    agent_frame = agent_results["most_similar_frame_file"]
    assert agent_frame == best_frame_jpg, f"Expected most_similar_frame_file to be {best_frame_jpg}, got {agent_frame}"

    agent_min_l2 = float(agent_results["min_l2_distance"])
    assert abs(agent_min_l2 - min_dist) < 1.0, f"min_l2_distance {agent_min_l2} is not within 1.0 of truth {min_dist}"

    agent_mean = float(agent_results["brightness_mean"])
    assert abs(agent_mean - mean_b) < 0.5, f"brightness_mean {agent_mean} is not within 0.5 of truth {mean_b}"

    agent_ci_lower = float(agent_results["brightness_ci_lower"])
    assert abs(agent_ci_lower - ci[0]) < 0.5, f"brightness_ci_lower {agent_ci_lower} is not within 0.5 of truth {ci[0]}"

    agent_ci_upper = float(agent_results["brightness_ci_upper"])
    assert abs(agent_ci_upper - ci[1]) < 0.5, f"brightness_ci_upper {agent_ci_upper} is not within 0.5 of truth {ci[1]}"