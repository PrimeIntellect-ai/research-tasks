# test_final_state.py
import os
import hashlib
import csv
import pytest

DATA_DIR = "/home/user/dataset"
CATS_DIR = "/home/user/categories"
RULES_FILE = "/home/user/rules.csv"

def get_file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def test_deduplication_and_categorization_score():
    # 1. Parse rules
    rules = []
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    cat_name = row[0].strip()
                    try:
                        min_size = int(row[1].strip())
                    except ValueError:
                        continue
                    magic_hex = row[2].strip().lower()
                    rules.append((cat_name, min_size, magic_hex))

    # 2. Analyze dataset for ideal sizes and expected categorizations
    total_logical_size = 0
    unique_contents = {} # hash -> size
    file_contents = {} # filename -> hash

    for f in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, f)
        if not os.path.isfile(path):
            continue

        st = os.stat(path)
        size = st.st_size
        total_logical_size += size

        file_hash = get_file_hash(path)
        file_contents[f] = file_hash

        if file_hash not in unique_contents:
            unique_contents[file_hash] = size

    ideal_physical_size = sum(unique_contents.values())

    # 3. Calculate actual physical size
    inodes = set()
    total_physical_size = 0
    for f in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, f)
        if not os.path.isfile(path):
            continue
        st = os.stat(path)
        if st.st_ino not in inodes:
            inodes.add(st.st_ino)
            total_physical_size += st.st_size

    # Space score
    if total_logical_size > ideal_physical_size:
        space_score = (total_logical_size - total_physical_size) / (total_logical_size - ideal_physical_size)
    else:
        space_score = 1.0
    space_score = min(max(space_score, 0.0), 1.0)

    # 4. Determine expected categorizations per unique content
    # For each unique content, which categories should it belong to?
    content_to_categories = {h: set() for h in unique_contents}

    # We need to read the magic bytes of each unique content
    # We can just pick one file for each hash
    hash_to_sample_file = {}
    for f, h in file_contents.items():
        if h not in hash_to_sample_file:
            hash_to_sample_file[h] = os.path.join(DATA_DIR, f)

    for h, sample_path in hash_to_sample_file.items():
        size = unique_contents[h]
        try:
            with open(sample_path, 'rb') as f:
                header = f.read(16).hex().lower()
        except Exception:
            header = ""

        for cat_name, min_size, magic_hex in rules:
            if size >= min_size and header.startswith(magic_hex):
                content_to_categories[h].add(cat_name)

    # 5. Evaluate actual symlinks
    actual_symlinks = [] # list of (category, target_hash)
    if os.path.exists(CATS_DIR):
        for cat_name in os.listdir(CATS_DIR):
            cat_path = os.path.join(CATS_DIR, cat_name)
            if not os.path.isdir(cat_path):
                continue
            for f in os.listdir(cat_path):
                link_path = os.path.join(cat_path, f)
                if os.path.islink(link_path):
                    target_path = os.path.realpath(link_path)
                    if target_path.startswith(DATA_DIR) and os.path.exists(target_path):
                        target_hash = get_file_hash(target_path)
                        actual_symlinks.append((cat_name, target_hash))

    # Calculate True Positives, False Positives, False Negatives
    # We evaluate at the level of unique contents to be fair to different deduplication strategies
    tp = 0
    fp = 0

    # Count actuals
    actual_content_cats = set(actual_symlinks)

    for cat_name, h in actual_content_cats:
        if cat_name in content_to_categories.get(h, set()):
            tp += 1
        else:
            fp += 1

    # Count false negatives
    fn = 0
    for h, expected_cats in content_to_categories.items():
        for cat_name in expected_cats:
            if (cat_name, h) not in actual_content_cats:
                fn += 1

    if (tp + fp) == 0:
        precision = 0.0
    else:
        precision = tp / (tp + fp)

    if (tp + fn) == 0:
        recall = 1.0 # No expected symlinks
    else:
        recall = tp / (tp + fn)

    if precision + recall == 0:
        f1_score = 0.0
    else:
        f1_score = 2 * precision * recall / (precision + recall)

    final_score = space_score * f1_score

    assert final_score >= 0.95, (
        f"Combined optimization score is too low: {final_score:.4f} < 0.95.\n"
        f"Space Score: {space_score:.4f} (Logical: {total_logical_size}, Physical: {total_physical_size}, Ideal: {ideal_physical_size})\n"
        f"Symlink F1 Score: {f1_score:.4f} (TP: {tp}, FP: {fp}, FN: {fn})"
    )