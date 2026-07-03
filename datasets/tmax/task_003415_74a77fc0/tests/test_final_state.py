# test_final_state.py
import os
import pytest

def test_organization_accuracy_score():
    orig_manifest_path = '/home/user/project_dump/manifest.txt'
    new_manifest_path = '/home/user/manifest_updated.txt'

    assert os.path.exists(orig_manifest_path), f"Original manifest missing at {orig_manifest_path}"
    assert os.path.exists(new_manifest_path), f"Updated manifest missing at {new_manifest_path}"

    with open(orig_manifest_path, 'r') as orig:
        orig_lines = orig.readlines()

    with open(new_manifest_path, 'r') as new_m:
        new_lines = new_m.readlines()

    assert len(orig_lines) == len(new_lines), "Updated manifest must have the same number of lines as the original manifest"

    total_valid = 0
    correct_mapped = 0

    for orig_l, new_l in zip(orig_lines, new_lines):
        orig_path_rel = orig_l.split('Asset: ')[1].strip()
        full_orig = os.path.join('/home/user/project_dump', orig_path_rel)

        assert os.path.exists(full_orig), f"Original file missing: {full_orig}"

        with open(full_orig, 'rb') as f:
            header = f.read(8)

        is_valid = False
        true_ext = ''
        if header.startswith(b'\x89PNG\x0d\x0a\x1a\x0a'):
            is_valid = True
            true_ext = 'png'
        elif header.startswith(b'\xff\xd8\xff'):
            is_valid = True
            true_ext = 'jpg'
        elif header.startswith(b'%PDF-'):
            is_valid = True
            true_ext = 'pdf'

        if is_valid:
            total_valid += 1
            new_path = new_l.split('Asset: ')[1].strip()
            # Check if it was mapped correctly
            if os.path.exists(new_path) and f"/organized/{true_ext}/" in new_path:
                correct_mapped += 1

    assert total_valid > 0, "No valid files found in the original dump. Setup might be corrupted."

    score = correct_mapped / total_valid

    assert score >= 0.95, f"Organization Accuracy Score is {score:.3f}, which is below the threshold of 0.95. Correctly mapped: {correct_mapped}/{total_valid}."