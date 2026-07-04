# test_final_state.py
import os
import tarfile
import subprocess
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

def calculate_ssim(img1, img2):
    """Compute Structural Similarity Index Measure (SSIM) between two images."""
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    mu1 = gaussian_filter(img1, sigma=1.5, truncate=3.5)
    mu2 = gaussian_filter(img2, sigma=1.5, truncate=3.5)

    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = gaussian_filter(img1 ** 2, sigma=1.5, truncate=3.5) - mu1_sq
    sigma2_sq = gaussian_filter(img2 ** 2, sigma=1.5, truncate=3.5) - mu2_sq
    sigma12 = gaussian_filter(img1 * img2, sigma=1.5, truncate=3.5) - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()

def test_final_archive_and_metrics():
    """Verify the final archive contents, file encodings, text replacements, and image quality (SSIM)."""
    agent_archive = '/home/user/docs_package.tar.gz'
    assert os.path.exists(agent_archive), f"Archive not found: {agent_archive}"

    extract_dir = '/tmp/agent_extract_test'
    os.makedirs(extract_dir, exist_ok=True)
    with tarfile.open(agent_archive, 'r:gz') as tar:
        tar.extractall(extract_dir)

    # Check text files for UTF-8 encoding and string replacement
    txt_files = [f for f in os.listdir(extract_dir) if f.endswith('.txt')]
    assert len(txt_files) > 0, "No .txt files found in the extracted archive."

    for txt_file in txt_files:
        filepath = os.path.join(extract_dir, txt_file)
        with open(filepath, 'rb') as f:
            content = f.read()
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                assert False, f"File {txt_file} is not valid UTF-8. Encoding conversion failed."

            assert 'AcmeCorp' not in text, f"Legacy text 'AcmeCorp' still found in {txt_file}."
            assert 'NovaTech' in text, f"Replacement text 'NovaTech' not found in {txt_file}."

    # Generate ground truth frames
    gt_dir = '/tmp/gt_frames_test'
    os.makedirs(gt_dir, exist_ok=True)
    times = [2, 4, 6, 8, 10]
    for t in times:
        subprocess.run(
            ['ffmpeg', '-y', '-ss', f'00:00:{t:02d}', '-i', '/app/demo_recording.mp4', '-frames:v', '1', '-q:v', '2', f'{gt_dir}/frame_{t}.jpg'],
            capture_output=True, check=True
        )

    # Calculate SSIM
    total_ssim = 0.0
    for t in times:
        agent_frame = os.path.join(extract_dir, f'frame_{t}.jpg')
        gt_frame = os.path.join(gt_dir, f'frame_{t}.jpg')
        assert os.path.exists(agent_frame), f"Extracted frame missing from archive: {agent_frame}"

        # Load and convert to grayscale
        img1 = np.array(Image.open(agent_frame).convert('L'))
        img2 = np.array(Image.open(gt_frame).convert('L'))

        # Ensure dimensions match before SSIM computation
        if img1.shape != img2.shape:
            img1_pil = Image.open(agent_frame).convert('L')
            img1 = np.array(img1_pil.resize((img2.shape[1], img2.shape[0])))

        score = calculate_ssim(img1, img2)
        total_ssim += score

    avg_ssim = total_ssim / len(times)
    assert avg_ssim >= 0.95, f"Average SSIM {avg_ssim:.4f} is below the required threshold of 0.95."