# test_final_state.py
import os
import tarfile
import subprocess
import numpy as np
import imageio.v3 as iio
from scipy.ndimage import gaussian_filter

def calculate_ssim(img1, img2):
    """
    Calculate Structural Similarity Index (SSIM) between two images.
    """
    if img1.shape != img2.shape:
        # If dimensions mismatch slightly due to different extraction methods, resize or fail
        return 0.0

    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    sigma = 1.5

    mu1 = gaussian_filter(img1, sigma)
    mu2 = gaussian_filter(img2, sigma)

    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = gaussian_filter(img1**2, sigma) - mu1_sq
    sigma2_sq = gaussian_filter(img2**2, sigma) - mu2_sq
    sigma12 = gaussian_filter(img1 * img2, sigma) - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    return np.mean(ssim_map)

def test_video_processing_ssim():
    archive_path = '/home/user/processed/tutorial_assets.tar.gz'
    assert os.path.exists(archive_path), f"Archive not found: {archive_path}"

    extract_dir = '/tmp/agent_frames'
    os.makedirs(extract_dir, exist_ok=True)
    with tarfile.open(archive_path, 'r:gz') as tar:
        tar.extractall(path=extract_dir)

    video_path = '/app/tutorial.mp4'
    duration_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    try:
        duration_str = subprocess.check_output(duration_cmd).decode('utf-8').strip()
        duration = float(duration_str)
    except Exception as e:
        assert False, f"Failed to get video duration: {e}"

    golden_dir = '/tmp/golden_frames'
    os.makedirs(golden_dir, exist_ok=True)

    percentages = [10, 20, 30, 40, 50, 60, 70, 80, 90, 99]
    ssim_scores = []

    for i, p in enumerate(percentages, 1):
        timestamp = duration * (p / 100.0)
        golden_img_path = f"{golden_dir}/fig_{i:02d}.jpg"

        # Generate golden frame
        subprocess.run([
            'ffmpeg', '-y', '-ss', str(timestamp), '-i', video_path, 
            '-frames:v', '1', '-q:v', '2', golden_img_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        agent_img_path = f"{extract_dir}/fig_{i:02d}.jpg"
        assert os.path.exists(agent_img_path), f"Agent image not found in archive: fig_{i:02d}.jpg"

        agent_img = iio.imread(agent_img_path)
        golden_img = iio.imread(golden_img_path)

        # Convert to grayscale
        if agent_img.ndim == 3:
            agent_img = np.dot(agent_img[...,:3], [0.2989, 0.5870, 0.1140])
        if golden_img.ndim == 3:
            golden_img = np.dot(golden_img[...,:3], [0.2989, 0.5870, 0.1140])

        score = calculate_ssim(golden_img, agent_img)
        ssim_scores.append(score)

    avg_ssim = sum(ssim_scores) / len(ssim_scores)
    assert avg_ssim >= 0.90, f"Average SSIM {avg_ssim:.4f} is below threshold 0.90"

def test_manifest_exists():
    archive_path = '/home/user/processed/tutorial_assets.tar.gz'
    assert os.path.exists(archive_path), f"Archive not found: {archive_path}"

    extract_dir = '/tmp/agent_frames'
    manifest_path = f"{extract_dir}/manifest.sha256"
    assert os.path.exists(manifest_path), "manifest.sha256 not found in extracted archive"

    with open(manifest_path, 'r') as f:
        lines = f.readlines()

    # Check that there are exactly 10 lines (or at least 10 entries for the images)
    jpg_lines = [line for line in lines if '.jpg' in line]
    assert len(jpg_lines) == 10, f"Expected 10 image checksums in manifest, found {len(jpg_lines)}"