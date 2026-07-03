# test_final_state.py
import os
import subprocess
import struct
import cv2
import pytest
from skimage.metrics import structural_similarity as ssim

def test_archive_size():
    archive_path = '/home/user/video_archive.bin'
    assert os.path.exists(archive_path), "Archive not found at /home/user/video_archive.bin"
    size = os.path.getsize(archive_path)
    assert size <= 5242880, f"Archive size {size} exceeds 5MB threshold"

def test_zip_slip_protection():
    archive_path = '/home/user/video_archive.bin'
    extract_script = '/home/user/extract.py'

    if not os.path.exists(extract_script):
        # Fallback if script is named differently or in /app
        if os.path.exists('/app/extract.py'):
            extract_script = '/app/extract.py'
        else:
            pytest.fail("extract.py script not found to test Zip Slip protection")

    # Append a malicious entry to the archive
    malicious_path = "../malicious_test_file.txt"
    malicious_data = b"malicious content"

    # Format: [Path Length (2 bytes, unsigned short)][File Path (UTF-8)][Data Length (4 bytes, unsigned int)][Compressed File Data]
    path_bytes = malicious_path.encode('utf-8')
    entry = struct.pack(f"<H{len(path_bytes)}sI", len(path_bytes), path_bytes, len(malicious_data)) + malicious_data

    with open(archive_path, 'ab') as f:
        f.write(entry)

    # Run extract.py
    subprocess.run(["python3", extract_script], capture_output=True)

    # Check if malicious file was extracted outside
    malicious_out_path = "/home/user/malicious_test_file.txt"
    assert not os.path.exists(malicious_out_path), "Zip Slip vulnerability detected: malicious file was extracted outside the target directory"

def test_restored_frames_ssim():
    video_path = '/app/surveillance.mp4'
    restored_dir = '/home/user/restored_frames'

    assert os.path.exists(restored_dir), "Restored frames directory not found"

    # Extract reference frames
    cap = cv2.VideoCapture(video_path)
    assert cap.isOpened(), "Could not open original video"

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps != fps:
        fps = 30.0 # fallback

    frame_interval = int(round(fps / 2.0))
    if frame_interval < 1:
        frame_interval = 1

    ref_frames = []
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            resized = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            # Convert to grayscale for SSIM
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            ref_frames.append(gray)
        count += 1
    cap.release()

    # Load restored frames
    restored_files = sorted([f for f in os.listdir(restored_dir) if f.endswith('.png') or f.endswith('.jpg')])
    assert len(restored_files) > 0, "No restored frames found"

    # We might have slight differences in frame counts, compare up to the minimum
    min_frames = min(len(ref_frames), len(restored_files))
    assert min_frames > 0, "No frames to compare"

    total_ssim = 0.0
    for i in range(min_frames):
        restored_path = os.path.join(restored_dir, restored_files[i])
        restored_img = cv2.imread(restored_path, cv2.IMREAD_GRAYSCALE)

        if restored_img is None:
            continue

        # Ensure dimensions match for SSIM
        if restored_img.shape != ref_frames[i].shape:
            restored_img = cv2.resize(restored_img, (ref_frames[i].shape[1], ref_frames[i].shape[0]))

        score, _ = ssim(ref_frames[i], restored_img, full=True)
        total_ssim += score

    avg_ssim = total_ssim / min_frames
    assert avg_ssim >= 0.90, f"Average SSIM {avg_ssim:.4f} is below the 0.90 threshold"