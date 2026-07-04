# test_final_state.py

import os
import glob
import hashlib
from collections import defaultdict

def get_files_in_dir(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def test_evil_corpus_rejected():
    evil_corpus_dir = "/app/corpus/evil"
    if not os.path.exists(evil_corpus_dir):
        return

    evil_tars = glob.glob(os.path.join(evil_corpus_dir, "*.tar"))
    bypassed = []

    for tar_path in evil_tars:
        dataset_name = os.path.basename(tar_path)[:-4]
        manifest_path = f"/home/user/pipeline/manifests/{dataset_name}.manifest"
        extracted_dir = f"/home/user/pipeline/extracted/{dataset_name}"

        if os.path.exists(manifest_path) or os.path.exists(extracted_dir):
            bypassed.append(dataset_name)

    assert not bypassed, f"{len(bypassed)} of {len(evil_tars)} evil bypassed: {bypassed}"

def test_clean_corpus_accepted():
    clean_corpus_dir = "/app/corpus/clean"
    if not os.path.exists(clean_corpus_dir):
        return

    clean_tars = glob.glob(os.path.join(clean_corpus_dir, "*.tar"))
    failed = []

    for tar_path in clean_tars:
        dataset_name = os.path.basename(tar_path)[:-4]
        manifest_path = f"/home/user/pipeline/manifests/{dataset_name}.manifest"
        extracted_dir = f"/home/user/pipeline/extracted/{dataset_name}"

        if not os.path.exists(manifest_path) or not os.path.exists(extracted_dir):
            failed.append(dataset_name)

    assert not failed, f"{len(failed)} of {len(clean_tars)} clean modified or rejected: {failed}"

def test_hardlinks_created_for_identical_files():
    extracted_base = "/home/user/pipeline/extracted"
    if not os.path.exists(extracted_base):
        return

    # Group files by their SHA256 hash
    content_map = defaultdict(list)

    for root, _, files in os.walk(extracted_base):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.isfile(file_path) or os.path.islink(file_path):
                continue

            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                hasher.update(f.read())
            file_hash = hasher.hexdigest()
            content_map[file_hash].append(file_path)

    # Check that identical files share the same inode (hardlinked)
    for file_hash, paths in content_map.items():
        if len(paths) > 1:
            inodes = {os.stat(p).st_ino for p in paths}
            assert len(inodes) == 1, f"Files with identical content are not hardlinked: {paths}"

            # Also check link count is > 1
            for p in paths:
                assert os.stat(p).st_nlink > 1, f"File {p} does not have link count > 1"