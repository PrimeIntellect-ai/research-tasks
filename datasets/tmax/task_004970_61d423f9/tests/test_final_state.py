# test_final_state.py

import os
import pytest

def test_final_answer_correct():
    answer_file = "/home/user/final_answer.txt"
    assert os.path.isfile(answer_file), f"Expected final answer file not found at {answer_file}"

    with open(answer_file, "r") as f:
        content = f.read().strip()

    # Recompute the expected value based on the original data intent
    vectors = [
        [1, 2, 3],
        [4, 5, 6],
        [-1, 0, 1],
        [2, -2, 2],
        [10, 20, 30]
    ]

    expected_sum = 0
    for i in range(len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        # Dot product is sum of products
        expected_sum += sum(a * b for a, b in zip(v1, v2))

    assert content == str(expected_sum), f"Expected the final answer to be '{expected_sum}', but got '{content}'"