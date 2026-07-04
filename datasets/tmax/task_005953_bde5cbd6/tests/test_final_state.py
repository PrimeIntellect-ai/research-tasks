# test_final_state.py
import json
import re
import math
import os

def test_output_exists_and_valid():
    output_path = '/home/user/output.json'
    corpus_path = '/home/user/corpus.txt'

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.exists(corpus_path), f"Corpus file {corpus_path} does not exist."

    with open(corpus_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    vocab_set = set()
    for line in lines:
        cleaned = re.sub(r'[^\w\s]', '', line.lower())
        tokens = cleaned.split()
        cleaned_lines.append(tokens)
        vocab_set.update(tokens)

    vocab = {word: i for i, word in enumerate(sorted(list(vocab_set)))}
    expected_vocab_size = len(vocab)

    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            output = json.load(f)
    except json.JSONDecodeError:
        assert False, f"{output_path} is not a valid JSON file."

    assert "vocab_size" in output, "Missing 'vocab_size' in output JSON."
    assert output["vocab_size"] == expected_vocab_size, f"Expected vocab_size {expected_vocab_size}, got {output['vocab_size']}."

    assert "first_5_lines" in output, "Missing 'first_5_lines' in output JSON."
    assert isinstance(output["first_5_lines"], list), "'first_5_lines' should be a list."
    assert len(output["first_5_lines"]) == 5, f"Expected 5 items in 'first_5_lines', got {len(output['first_5_lines'])}."

    # Pre-computed means based on numpy.random.seed(42) and uniform(-1, 1, (43, 16))
    expected_means = [0.1746, -0.1983, -0.6276, -0.1633, 0.2885]

    for i in range(5):
        item = output["first_5_lines"][i]
        assert "line_index" in item, f"Missing 'line_index' in item {i}."
        assert item["line_index"] == i, f"Expected line_index {i}, got {item['line_index']}."

        expected_tokens = [vocab[t] for t in cleaned_lines[i]]
        assert "token_ids" in item, f"Missing 'token_ids' in item {i}."
        assert item["token_ids"] == expected_tokens, f"Expected token_ids {expected_tokens} for line {i}, got {item['token_ids']}."

        assert "embedding_sum_mean" in item, f"Missing 'embedding_sum_mean' in item {i}."
        mean_val = item["embedding_sum_mean"]
        assert isinstance(mean_val, float), f"'embedding_sum_mean' should be a float for line {i}."

        # Check if the float has exactly 4 decimal places (by checking its string representation if needed, 
        # but mathematical closeness to the rounded value is more robust).
        assert math.isclose(mean_val, expected_means[i], abs_tol=1e-4), \
            f"Expected embedding_sum_mean close to {expected_means[i]} for line {i}, got {mean_val}."