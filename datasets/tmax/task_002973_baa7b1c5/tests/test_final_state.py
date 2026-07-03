# test_final_state.py
import os
import pytest

def test_directory_state_accuracy():
    """
    Evaluates the directory state accuracy metric as defined in the verifier.
    Target value is 1.0.
    """
    score = 0.0

    # 1. Check DOC_evil.txt
    evil_path = '/home/user/docs_clean/DOC_evil.txt'
    if os.path.exists(evil_path):
        try:
            with open(evil_path, 'r') as f:
                if 'PUBLISHED document' in f.read():
                    score += 0.25
        except Exception:
            pass

    # 2. Check DOC_valid_doc.md
    valid_path = '/home/user/docs_clean/DOC_valid_doc.md'
    if os.path.exists(valid_path):
        try:
            with open(valid_path, 'r') as f:
                if 'This is in PUBLISHED.' in f.read():
                    score += 0.25
        except Exception:
            pass

    # 3. Check DOC_image_file.png
    img_path = '/home/user/docs_clean/DOC_image_file.png'
    if os.path.exists(img_path):
        try:
            with open(img_path, 'rb') as f:
                header = f.read(8)
                if header == b'\x89PNG\r\n\x1a\n':
                    score += 0.25
        except Exception:
            pass

    # 4. Check no zip slip occurred
    if not os.path.exists('/home/etc/evil.txt') and not os.path.exists('/etc/evil.txt'):
        score += 0.25

    assert score >= 1.0, f"Score {score} is below the threshold of 1.0. Ensure all instructions were applied correctly and zip slip was prevented."