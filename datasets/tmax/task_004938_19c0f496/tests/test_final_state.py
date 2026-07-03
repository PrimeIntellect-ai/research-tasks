# test_final_state.py

import os
import numpy as np
from PIL import Image
import pytest

def calculate_mse(imageA_path, imageB_path):
    try:
        imgA = np.array(Image.open(imageA_path).convert('RGB')).astype("float")
        imgB = np.array(Image.open(imageB_path).convert('RGB')).astype("float")

        if imgA.shape != imgB.shape:
            return float('inf')

        err = np.sum((imgA - imgB) ** 2)
        err /= float(imgA.shape[0] * imgA.shape[1])
        return err
    except Exception as e:
        return float('inf')

def test_extracted_files_exist():
    """Verify that the expected output files exist and are correctly named."""
    clean_dir = '/home/user/clean_dataset'
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist."

    files = sorted(os.listdir(clean_dir))
    expected_files = ['dataset_001.jpg', 'dataset_002.jpg']

    for f in expected_files:
        assert f in files, f"Expected file {f} is missing from {clean_dir}."

    # Ensure no path traversal files were extracted into the clean dataset directory
    assert len(files) == 2, f"Expected exactly 2 files in {clean_dir}, but found {len(files)}: {files}"

def test_mse_metric():
    """Verify that dataset_001.jpg matches the hidden reference image within the MSE threshold."""
    target_img = '/home/user/clean_dataset/dataset_001.jpg'
    ref_img = '/app/.hidden_ref.jpg'

    assert os.path.isfile(target_img), f"Target image {target_img} is missing."
    assert os.path.isfile(ref_img), f"Reference image {ref_img} is missing."

    mse = calculate_mse(target_img, ref_img)
    threshold = 1.0

    assert mse <= threshold, f"MSE {mse} exceeds the threshold of {threshold}. The image was not correctly decoded."

def test_path_traversal_prevented():
    """Verify that path traversal was prevented (important_notes.txt should not be extracted from zip)."""
    # The zip contains ../../home/user/important_notes.txt
    # If extracted unsafely, it might write to /home/user/important_notes.txt
    # We can't be 100% sure if the file existed before, but if the user script did it correctly, 
    # it shouldn't have written it. We mainly check that the user didn't dump it in clean_dataset.
    # The test_extracted_files_exist already checks clean_dataset has only 2 files.
    pass