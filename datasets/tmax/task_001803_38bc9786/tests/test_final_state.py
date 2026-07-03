# test_final_state.py
import os
import subprocess
import pytest
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

def calculate_ssim(img1, img2):
    """
    Computes the Structural Similarity Index (SSIM) between two images.
    Approximates skimage.metrics.structural_similarity.
    """
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    ssim_channels = []
    for i in range(img1.shape[2]):
        im1 = img1[:, :, i].astype(np.float64)
        im2 = img2[:, :, i].astype(np.float64)

        mu1 = gaussian_filter(im1, 1.5)
        mu2 = gaussian_filter(im2, 1.5)

        mu1_sq = mu1**2
        mu2_sq = mu2**2
        mu1_mu2 = mu1 * mu2

        sigma1_sq = gaussian_filter(im1**2, 1.5) - mu1_sq
        sigma2_sq = gaussian_filter(im2**2, 1.5) - mu2_sq
        sigma12 = gaussian_filter(im1 * im2, 1.5) - mu1_mu2

        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
        ssim_channels.append(ssim_map.mean())

    return np.mean(ssim_channels)

def test_mre_parse_exists():
    assert os.path.isfile("/workspace/vid_project/mre_parse.py"), "mre_parse.py is missing. You must create a minimal reproducible example."

def test_extracted_frames_ssim():
    agent_dir = "/workspace/output_frames"
    gt_dir = "/tmp/gt_frames"
    video_path = "/app/test_video.mp4"

    assert os.path.isfile(video_path), f"Video fixture {video_path} is missing."

    # Generate ground truth
    os.makedirs(gt_dir, exist_ok=True)
    subprocess.run([
        'ffmpeg', '-i', video_path, '-vf', 
        "select='eq(n,10)+eq(n,20)+eq(n,30)'", '-vsync', '0', 
        f'{gt_dir}/frame_%d.jpg', '-y'
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    assert os.path.isdir(agent_dir), f"Agent output directory {agent_dir} does not exist."

    agent_files = sorted([f for f in os.listdir(agent_dir) if f.endswith('.jpg')])
    gt_files = sorted([f for f in os.listdir(gt_dir) if f.endswith('.jpg')])

    assert len(agent_files) > 0, "No jpg files found in agent output directory."
    assert len(agent_files) == len(gt_files), f"Count mismatch. Expected {len(gt_files)} frames, got {len(agent_files)}."

    ssim_scores = []
    for af, gf in zip(agent_files, gt_files):
        img_a = np.array(Image.open(os.path.join(agent_dir, af)).convert('RGB'))
        img_g = np.array(Image.open(os.path.join(gt_dir, gf)).convert('RGB'))

        # Resize if dimensions differ slightly due to backend differences
        if img_a.shape != img_g.shape:
            img_a_pil = Image.fromarray(img_a).resize((img_g.shape[1], img_g.shape[0]), Image.LANCZOS)
            img_a = np.array(img_a_pil)

        score = calculate_ssim(img_a, img_g)
        ssim_scores.append(score)

    avg_ssim = np.mean(ssim_scores)
    assert avg_ssim >= 0.95, f"SSIM {avg_ssim:.4f} is below threshold 0.95. Extracted frames do not match ground truth closely enough."