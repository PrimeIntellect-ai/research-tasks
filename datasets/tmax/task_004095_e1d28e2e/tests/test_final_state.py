# test_final_state.py
import os
import glob
import json
import pytest

def test_json_files_exist_and_valid():
    processed_dir = "/home/user/processed"
    json_files = glob.glob(os.path.join(processed_dir, "*.json"))
    assert len(json_files) == 200, f"Expected 200 .json files in {processed_dir}, found {len(json_files)}"

    for jf in json_files:
        with open(jf, 'r') as f:
            try:
                # Use object_pairs_hook to preserve the order of keys as they appear in the file
                pairs = json.load(f, object_pairs_hook=list)
            except json.JSONDecodeError:
                pytest.fail(f"File {jf} is not valid JSON.")

        # Check flat structure
        assert isinstance(pairs, list), f"File {jf} does not contain a JSON object."

        keys = []
        for k, v in pairs:
            assert isinstance(v, str), f"Value for key '{k}' in {jf} is not a string."
            keys.append(k)

        # Check if keys are sorted alphabetically
        assert keys == sorted(keys), f"Keys in {jf} are not sorted alphabetically. Found: {keys}"

def test_compression_ratio():
    original_dir = '/home/user/configs'
    processed_dir = '/home/user/processed'

    orig_files = glob.glob(os.path.join(original_dir, "*.conf"))
    comp_files = glob.glob(os.path.join(processed_dir, "*.jc"))

    assert len(orig_files) == 200, f"Expected 200 original .conf files, found {len(orig_files)}"
    assert len(comp_files) == 200, f"Expected 200 compressed .jc files in {processed_dir}, found {len(comp_files)}"

    orig_size = sum(os.path.getsize(f) for f in orig_files)
    comp_size = sum(os.path.getsize(f) for f in comp_files)

    assert comp_size > 0, "Total size of compressed files is 0, compression failed."

    ratio = orig_size / comp_size
    assert ratio >= 2.8, f"Compression ratio {ratio:.2f} is below the threshold of 2.8. Ensure noise is removed and keys are sorted."