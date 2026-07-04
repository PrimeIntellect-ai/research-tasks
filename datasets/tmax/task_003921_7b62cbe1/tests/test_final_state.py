# test_final_state.py

import os
import tarfile
import subprocess
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
import pytest

def compute_ssim(img1, img2):
    """Compute Structural Similarity Index (SSIM) between two images."""
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
    return ssim_map.mean()

def extract_reference_frames():
    """Extract golden frames directly from the video to compare against."""
    os.makedirs("/tmp/golden_frames", exist_ok=True)
    for f in range(0, 1001, 25):
        cmd = f"ffmpeg -i /app/experiment.mp4 -vf 'select=eq(n\\,{f})' -vsync vfr -q:v 2 /tmp/golden_frames/frame_{f}.jpg -y"
        subprocess.run(cmd, shell=True, capture_output=True)

def test_final_state():
    # 1. Extract golden frames
    extract_reference_frames()

    curated_dir = "/home/user/curated_dataset"
    assert os.path.isdir(curated_dir), f"Curated directory not found at {curated_dir}"

    total_ssim = 0.0
    count = 0

    # 2. Evaluate SSIM for all expected frames
    for f in range(0, 1001, 25):
        padded_idx = str(f).zfill(6)
        agent_img = os.path.join(curated_dir, f"sample_{padded_idx}.jpg")
        golden_img = f"/tmp/golden_frames/frame_{f}.jpg"

        assert os.path.exists(golden_img), f"Test setup failed to extract golden frame {f}"

        if os.path.exists(agent_img):
            imgA = np.array(Image.open(golden_img).convert('L'))
            imgB = Image.open(agent_img).convert('L')

            # Resize imgB to imgA's shape (width, height) to tolerate minor codec/resolution differences
            imgB = imgB.resize((imgA.shape[1], imgA.shape[0]))
            imgB = np.array(imgB)

            score = compute_ssim(imgA, imgB)
            total_ssim += score
        else:
            pytest.fail(f"Missing expected extracted frame at {agent_img}")

        count += 1

    avg_ssim = total_ssim / count if count > 0 else 0.0

    # 3. Verify backup archive
    backup_path = "/home/user/dataset_backup.tar.gz"
    assert os.path.exists(backup_path), f"Backup archive not found at {backup_path}"

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            members = tar.getmembers()
            # Expecting at least 41 frames + 41 JSONs = 82 files, but set a safe lower bound of 40
            assert len(members) >= 40, f"Archive contains too few members ({len(members)}). It should contain the dataset."
    except Exception as e:
        pytest.fail(f"Failed to open or validate archive {backup_path}: {e}")

    # 4. Assert the final metric
    assert avg_ssim >= 0.95, f"Average SSIM {avg_ssim:.4f} is below the threshold of 0.95"