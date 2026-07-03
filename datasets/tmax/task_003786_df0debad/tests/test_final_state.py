# test_final_state.py

import os
import glob
import pytest

def test_done_file_exists():
    assert os.path.isfile("/app/DONE"), "The /app/DONE file is missing. The pipeline did not complete successfully."

def test_curated_symlinks():
    curated_dir = "/app/dataset/curated/"
    assert os.path.isdir(curated_dir), f"Directory missing: {curated_dir}"

    # Based on the truth data, timestamps are 1.50, 5.25, 12.10, 15.00.
    # Strictly greater than 10.0 seconds means 12.10 and 15.00.
    expected_links = {"frame_12.10.jpg", "frame_15.00.jpg"}

    actual_files = set(os.listdir(curated_dir))
    assert actual_files == expected_links, f"Expected curated symlinks {expected_links}, but found {actual_files}"

    for link in expected_links:
        link_path = os.path.join(curated_dir, link)
        assert os.path.islink(link_path), f"Expected {link_path} to be a symbolic link."

        target = os.readlink(link_path)
        # The target should point to the frame in /app/dataset/frames/
        assert os.path.basename(target) == link, f"Symlink {link_path} points to an incorrect target: {target}"

def test_frames_ssim():
    # Attempt to import cv2 and skimage as used in the truth verification script
    try:
        import cv2
        from skimage.metrics import structural_similarity as ssim

        def compute_ssim(img1_path, img2_path):
            img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
            if img1 is None or img2 is None:
                return 0.0
            if img1.shape != img2.shape:
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
            score, _ = ssim(img1, img2, full=True)
            return score

    except ImportError:
        # Fallback using PIL and numpy if cv2/skimage are somehow not available
        import numpy as np
        from PIL import Image

        def compute_ssim(img1_path, img2_path):
            try:
                img1 = np.array(Image.open(img1_path).convert('L'), dtype=np.float32)
                img2 = Image.open(img2_path).convert('L')
                if img1.shape != (img2.size[1], img2.size[0]):
                    img2 = img2.resize((img1.shape[1], img1.shape[0]))
                img2 = np.array(img2, dtype=np.float32)

                # Simplified score for fallback
                mse = np.mean((img1 - img2) ** 2)
                if mse == 0:
                    return 1.0
                return max(0.0, 1.0 - (mse / (255.0 ** 2)))
            except Exception:
                return 0.0

    golden_frames_dir = "/app/.hidden_truth/frames/"
    agent_frames_dir = "/app/dataset/frames/"

    golden_files = glob.glob(os.path.join(golden_frames_dir, "*.jpg"))
    assert len(golden_files) > 0, f"No golden frames found in {golden_frames_dir}"

    total_ssim = 0.0
    for gf in golden_files:
        basename = os.path.basename(gf)
        af = os.path.join(agent_frames_dir, basename)
        if os.path.exists(af):
            total_ssim += compute_ssim(gf, af)

    mean_ssim = total_ssim / len(golden_files)
    assert mean_ssim >= 0.95, f"Mean SSIM is {mean_ssim:.4f}, which is below the required threshold of 0.95."