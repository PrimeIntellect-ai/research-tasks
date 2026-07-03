# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_video_figure_extraction():
    images_dir = "/home/user/docs/images"
    expected_images = ["figure_1.jpg", "figure_2.jpg", "figure_3.jpg"]

    for img in expected_images:
        img_path = os.path.join(images_dir, img)
        assert os.path.isfile(img_path), f"Expected extracted frame {img_path} is missing."

        # Verify it's a valid JPEG by checking the magic number
        with open(img_path, 'rb') as f:
            header = f.read(2)
            assert header == b'\xff\xd8', f"File {img_path} is not a valid JPEG image."

def test_leak_detector_adversarial_corpus():
    # Find the detector script
    scripts = glob.glob("/home/user/docs/leak_detector.*")
    assert len(scripts) > 0, "No leak detector script found matching /home/user/docs/leak_detector.*"

    # Prefer the first one found, assuming it's the intended script
    script_path = scripts[0]

    # Ensure it's executable
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

    evil_corpus_path = "/app/corpus/evil/"
    clean_corpus_path = "/app/corpus/clean/"

    evil_files = [os.path.join(evil_corpus_path, f) for f in os.listdir(evil_corpus_path) if os.path.isfile(os.path.join(evil_corpus_path, f))]
    clean_files = [os.path.join(clean_corpus_path, f) for f in os.listdir(clean_corpus_path) if os.path.isfile(os.path.join(clean_corpus_path, f))]

    assert len(evil_files) > 0, "Evil corpus is empty."
    assert len(clean_files) > 0, "Clean corpus is empty."

    bypassed_evil = []
    modified_clean = []

    # Test evil corpus
    for file_path in evil_files:
        result = subprocess.run([script_path, file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(file_path))

    # Test clean corpus
    for file_path in clean_files:
        result = subprocess.run([script_path, file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(file_path))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    if error_msgs:
        pytest.fail("Adversarial corpus failed: " + " | ".join(error_msgs))