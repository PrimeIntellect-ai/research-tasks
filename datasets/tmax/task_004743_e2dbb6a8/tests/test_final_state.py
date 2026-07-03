# test_final_state.py
import os
import re
from collections import Counter

def test_final_state():
    high_dir = "/home/user/high_relevance"
    low_dir = "/home/user/low_relevance"

    assert os.path.isdir(high_dir), f"Directory {high_dir} is missing. The task requires creating it."
    assert os.path.isdir(low_dir), f"Directory {low_dir} is missing. The task requires creating it."

    # Collect all text files from the output directories to rebuild the corpus
    files = {}
    for d in [high_dir, low_dir]:
        for fname in os.listdir(d):
            if fname.endswith(".txt"):
                with open(os.path.join(d, fname), 'r') as f:
                    files[fname] = f.read()

    assert len(files) == 5, f"Expected exactly 5 .txt files across high/low relevance directories, but found {len(files)}. Did you move all files?"

    # Process text: punctuation to spaces, lowercase
    def extract_words(text):
        # Replace punctuation with spaces
        text = re.sub(r'[^\w\s]', ' ', text).lower()
        # Strictly alphanumeric and length > 2
        return [w for w in text.split() if len(w) > 2 and w.isalnum() and not w.isdigit()]

    all_words = []
    for content in files.values():
        all_words.extend(extract_words(content))

    counts = Counter(all_words)
    # Sort by frequency (descending), then alphabetically (ascending)
    sorted_words = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    top_5 = sorted_words[:5]

    # Assign weights: Rank 1 -> 5, Rank 2 -> 4, etc.
    weights = {top_5[i][0]: 5 - i for i in range(len(top_5))}

    expected_scores = {}
    for fname, content in files.items():
        f_words = extract_words(content)
        f_counts = Counter(f_words)
        score = sum(f_counts[w] * weights.get(w, 0) for w in weights)
        expected_scores[fname] = score

    # Verify file locations based on recomputed scores
    for fname, score in expected_scores.items():
        if score >= 15:
            expected_path = os.path.join(high_dir, fname)
            assert os.path.exists(expected_path), f"File {fname} has a score of {score} (>= 15) and should be in {high_dir}."
        else:
            expected_path = os.path.join(low_dir, fname)
            assert os.path.exists(expected_path), f"File {fname} has a score of {score} (< 15) and should be in {low_dir}."

    # Verify the log file
    log_path = "/home/user/scores.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        log_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected_log = [f"{fname}:{score}" for fname, score in sorted(expected_scores.items())]

    assert log_lines == expected_log, (
        f"Log file {log_path} contents do not match expected output.\n"
        f"Expected: {expected_log}\n"
        f"Got: {log_lines}"
    )