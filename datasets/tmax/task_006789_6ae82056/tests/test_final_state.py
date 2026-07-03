# test_final_state.py
import os
import json

def test_features_csv_exists_and_correct():
    csv_path = "/home/user/features.csv"
    assert os.path.exists(csv_path), f"{csv_path} does not exist. The Rust program may not have run successfully or output to the wrong location."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    raw_path = "/home/user/raw_data.jsonl"
    assert os.path.exists(raw_path), f"{raw_path} is missing. Did you delete or move the input data?"

    expected_rows = []
    with open(raw_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Schema enforcement: doc_id must be u32 (non-negative int), content must be string
            if "doc_id" not in data or "content" not in data:
                continue
            # Also ensure no extra fields by strict schema if needed, but rubric just says "missing fields, wrong types"
            if not isinstance(data["doc_id"], int) or isinstance(data["doc_id"], bool) or data["doc_id"] < 0:
                continue
            if not isinstance(data["content"], str):
                continue

            # Tokenization and hashing
            doc_id = data["doc_id"]
            content = data["content"].lower()
            tokens = content.split()

            f_counts = [0, 0, 0, 0]
            for token in tokens:
                ascii_sum = sum(ord(c) for c in token)
                f_counts[ascii_sum % 4] += 1

            expected_rows.append((doc_id, f_counts))

    # Sort by doc_id ascending
    expected_rows.sort(key=lambda x: x[0])

    expected_csv_lines = ["doc_id,f0,f1,f2,f3"]
    for doc_id, counts in expected_rows:
        expected_csv_lines.append(f"{doc_id},{counts[0]},{counts[1]},{counts[2]},{counts[3]}")

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_csv_lines, (
        f"CSV content mismatch.\n"
        f"Expected {len(expected_csv_lines)} lines, got {len(actual_lines)} lines.\n"
        f"Expected:\n{expected_csv_lines}\n"
        f"Got:\n{actual_lines}"
    )