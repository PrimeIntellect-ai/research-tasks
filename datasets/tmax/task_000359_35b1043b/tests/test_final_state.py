# test_final_state.py
import os
import math
import pytest

def test_metrics_file_and_perplexity():
    # Reconstruct reference Perplexity
    train_seqs = [
        ['A', 'B', 'C', 'D', 'E'],
        ['A', 'A', 'B', 'C'],
        ['B', 'D', 'E', 'A'],
        ['C', 'E', 'E'],
        ['A', 'B', 'D'],
        ['E', 'D', 'C', 'B', 'A'],
        ['A', 'C', 'E'],
        ['B', 'B', 'B'],
        ['D', 'A', 'C'],
        ['E', 'A', 'B', 'C', 'D']
    ]

    test_seqs = [
        ['A', 'B', 'E'],
        ['C', 'D', 'A'],
        ['E', 'E']
    ]

    vocab = ['A', 'B', 'C', 'D', 'E']
    V = 5

    bigram_counts = {u: {v: 0 for v in vocab} for u in ['<s>'] + vocab}
    unigram_counts = {u: 0 for u in ['<s>'] + vocab}

    for seq in train_seqs:
        prev = '<s>'
        unigram_counts[prev] += 1
        for token in seq:
            bigram_counts[prev][token] += 1
            unigram_counts[token] += 1
            prev = token

    total_log_prob = 0.0
    total_tokens = 0

    for seq in test_seqs:
        prev = '<s>'
        for token in seq:
            count_uv = bigram_counts[prev][token]
            count_u = unigram_counts[prev]

            prob = (count_uv + 1) / (count_u + V)
            total_log_prob += math.log2(prob)
            total_tokens += 1
            prev = token

    ref_perplexity = 2 ** (- (total_log_prob / total_tokens))

    metrics_path = '/home/user/metrics.txt'
    assert os.path.exists(metrics_path), f"Output file {metrics_path} does not exist."

    with open(metrics_path, 'r') as f:
        content = f.read()

    agent_perp = None
    for line in content.split('\n'):
        if line.startswith('Test_Perplexity:'):
            try:
                agent_perp = float(line.split(':')[1].strip())
            except ValueError:
                pytest.fail("Test_Perplexity value could not be parsed as a float.")
            break

    assert agent_perp is not None, "Could not find 'Test_Perplexity:' line in metrics.txt"

    error = abs(agent_perp - ref_perplexity)

    assert error <= 0.05, (
        f"Test_Perplexity error {error:.4f} is greater than threshold 0.05. "
        f"Reference Perplexity: {ref_perplexity:.4f}, Agent Perplexity: {agent_perp:.4f}"
    )