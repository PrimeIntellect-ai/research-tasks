# test_final_state.py
import os
import re

def compute_alignment_scores(primer, targets):
    scores = []
    k = len(primer)
    for t in targets:
        max_score = 0
        for i in range(len(t) - k + 1):
            sub = t[i:i+k]
            score = sum(1 for a, b in zip(primer, sub) if a == b)
            if score > max_score:
                max_score = score
        scores.append(max_score)
    return scores

def test_results_file_exists_and_format():
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"Results file not found: {results_path}"

    with open(results_path, 'r') as f:
        content = f.read()

    expected_keys = [
        "CI_A_LOWER", "CI_A_UPPER",
        "CI_B_LOWER", "CI_B_UPPER",
        "VAR_A", "VAR_B",
        "P_VALUE"
    ]

    parsed_values = {}
    for key in expected_keys:
        match = re.search(rf"^{key}=([0-9\.]+)", content, re.MULTILINE)
        assert match is not None, f"Key {key} not found or invalid format in results.txt"
        parsed_values[key] = float(match.group(1))

    # Basic sanity checks on the values
    assert parsed_values["CI_A_LOWER"] <= parsed_values["CI_A_UPPER"], "CI_A_LOWER > CI_A_UPPER"
    assert parsed_values["CI_B_LOWER"] <= parsed_values["CI_B_UPPER"], "CI_B_LOWER > CI_B_UPPER"
    assert parsed_values["VAR_A"] >= 0, "VAR_A is negative"
    assert parsed_values["VAR_B"] >= 0, "VAR_B is negative"
    assert 0 <= parsed_values["P_VALUE"] <= 1, "P_VALUE is out of bounds [0, 1]"

    # Recompute scores to check if CIs are reasonable
    targets_path = "/home/user/targets.txt"
    if os.path.isfile(targets_path):
        with open(targets_path, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]

        scores_a = compute_alignment_scores("ATGCGTGA", targets)
        scores_b = compute_alignment_scores("TCGATCCA", targets)

        mean_a = sum(scores_a) / len(scores_a)
        mean_b = sum(scores_b) / len(scores_b)

        # The true mean should be inside or very close to the 95% CI bounds
        assert parsed_values["CI_A_LOWER"] - 0.2 <= mean_a <= parsed_values["CI_A_UPPER"] + 0.2, \
            f"Mean of A ({mean_a}) is too far from CI [{parsed_values['CI_A_LOWER']}, {parsed_values['CI_A_UPPER']}]"
        assert parsed_values["CI_B_LOWER"] - 0.2 <= mean_b <= parsed_values["CI_B_UPPER"] + 0.2, \
            f"Mean of B ({mean_b}) is too far from CI [{parsed_values['CI_B_LOWER']}, {parsed_values['CI_B_UPPER']}]"