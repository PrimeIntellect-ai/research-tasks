# test_final_state.py
import json
import os
import math
import tarfile
import unicodedata
from collections import defaultdict

def get_expected_data():
    raw_file = "/home/user/translations_raw.jsonl"
    assert os.path.exists(raw_file), f"Missing raw file: {raw_file}"

    records = []
    with open(raw_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    # 1. Normalize and deduplicate
    dedup_map = {}
    for r in records:
        key = (r.get('context_key'), r.get('lang'))
        r['target'] = unicodedata.normalize('NFKC', r.get('target', ''))

        if key not in dedup_map:
            dedup_map[key] = r
        else:
            if r.get('timestamp', '') > dedup_map[key].get('timestamp', ''):
                dedup_map[key] = r

    dedup_records = list(dedup_map.values())

    # 2. Add month
    for r in dedup_records:
        r['month'] = r.get('timestamp', '')[:7]

    # 3. Stratified sampling
    groups = defaultdict(list)
    for r in dedup_records:
        groups[(r['month'], r['lang'])].append(r)

    review_records = []
    for (month, lang), group in groups.items():
        group.sort(key=lambda x: x['context_key'])
        n_sample = math.ceil(len(group) * 0.2)
        review_records.extend(group[:n_sample])

    return dedup_records, review_records

def test_remote_sync_archive():
    archive_path = "/home/user/remote_sync/translations_archive.tar.gz"
    assert os.path.exists(archive_path), f"Archive not found in remote_sync: {archive_path}"

    with tarfile.open(archive_path, 'r:gz') as tar:
        names = [os.path.basename(n) for n in tar.getnames()]
        assert 'translations_dedup.jsonl' in names, "translations_dedup.jsonl missing from tar archive"
        assert 'translations_review.jsonl' in names, "translations_review.jsonl missing from tar archive"

def test_dedup_file_content():
    dedup_file = "/home/user/translations_dedup.jsonl"
    assert os.path.exists(dedup_file), f"Missing dedup file: {dedup_file}"

    expected_dedup, _ = get_expected_data()

    actual_dedup = []
    with open(dedup_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                # Check JSON key sorting
                assert line.strip() == json.dumps(json.loads(line), sort_keys=True, ensure_ascii=False), "JSON keys in translations_dedup.jsonl are not sorted alphabetically."
                actual_dedup.append(json.loads(line))

    assert len(actual_dedup) == len(expected_dedup), f"Expected {len(expected_dedup)} deduplicated records, got {len(actual_dedup)}"

    # Compare content
    expected_dedup_sorted = sorted(expected_dedup, key=lambda x: (x.get('context_key', ''), x.get('lang', '')))
    actual_dedup_sorted = sorted(actual_dedup, key=lambda x: (x.get('context_key', ''), x.get('lang', '')))

    for exp, act in zip(expected_dedup_sorted, actual_dedup_sorted):
        assert exp == act, f"Mismatch in deduplicated record.\nExpected: {exp}\nGot: {act}"

def test_review_file_content():
    review_file = "/home/user/translations_review.jsonl"
    assert os.path.exists(review_file), f"Missing review file: {review_file}"

    _, expected_review = get_expected_data()

    actual_review = []
    with open(review_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                # Check JSON key sorting
                assert line.strip() == json.dumps(json.loads(line), sort_keys=True, ensure_ascii=False), "JSON keys in translations_review.jsonl are not sorted alphabetically."
                actual_review.append(json.loads(line))

    assert len(actual_review) == len(expected_review), f"Expected {len(expected_review)} review records, got {len(actual_review)}"

    # Compare content
    expected_review_sorted = sorted(expected_review, key=lambda x: (x.get('context_key', ''), x.get('lang', '')))
    actual_review_sorted = sorted(actual_review, key=lambda x: (x.get('context_key', ''), x.get('lang', '')))

    for exp, act in zip(expected_review_sorted, actual_review_sorted):
        assert exp == act, f"Mismatch in review record.\nExpected: {exp}\nGot: {act}"