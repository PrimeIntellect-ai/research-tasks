# test_final_state.py
import os
import cv2
from skimage.metrics import structural_similarity as ssim

def test_final_output_ssim():
    student_img_path = '/home/user/final_output.png'
    ref_img_path = '/tmp/reference_truth.png'

    assert os.path.isfile(student_img_path), f"Student output {student_img_path} not found."
    assert os.path.isfile(ref_img_path), f"Reference truth {ref_img_path} not found."

    img1 = cv2.imread(student_img_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(ref_img_path, cv2.IMREAD_GRAYSCALE)

    assert img1 is not None, f"Failed to read {student_img_path}"
    assert img2 is not None, f"Failed to read {ref_img_path}"

    # Resize if necessary to match dimensions for SSIM, though they should be identical
    if img1.shape != img2.shape:
        img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))

    score, _ = ssim(img1, img2, full=True)
    assert score >= 0.98, f"SSIM score {score:.4f} is below the threshold of 0.98"

def test_regression_script_exists():
    script_path = '/home/user/test_regression.sh'
    assert os.path.isfile(script_path), f"Regression test script {script_path} not found."
    assert os.access(script_path, os.X_OK), f"Regression test script {script_path} is not executable."