# test_final_state.py

import os
import json

def test_venv_exists():
    """Check if the virtual environment was created."""
    venv_dir = "/home/user/venv"
    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} is missing."

    # Check for python executable in venv
    python_bin = os.path.join(venv_dir, "bin", "python")
    assert os.path.isfile(python_bin), f"Python executable not found in venv at {python_bin}."

def test_output_json_exists():
    """Check if the output.json file exists."""
    output_path = "/home/user/output.json"
    assert os.path.isfile(output_path), f"File {output_path} is missing."

def test_output_json_content():
    """Validate the contents and computed values of output.json."""
    output_path = "/home/user/output.json"
    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {output_path} is not a valid JSON file."

    # Verify required keys
    required_keys = [
        "num_filtered_sequences",
        "max_hamming_distance",
        "top_singular_value",
        "t_statistic",
        "p_value"
    ]
    for key in required_keys:
        assert key in data, f"Key '{key}' is missing from output.json."

    # Re-compute deterministic parts in pure Python
    fasta_path = "/home/user/data/seqs.fasta"
    seqs = {}
    with open(fasta_path, 'r') as f:
        curr_id = None
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                curr_id = line[1:]
            elif curr_id:
                seqs[curr_id] = line
                curr_id = None

    # Filter sequences
    filtered_seqs = {k: v for k, v in seqs.items() if "GATCA" in v}
    sorted_keys = sorted(filtered_seqs.keys())

    expected_num_filtered = len(sorted_keys)
    assert data["num_filtered_sequences"] == expected_num_filtered, \
        f"Incorrect num_filtered_sequences. Expected {expected_num_filtered}, got {data['num_filtered_sequences']}."

    # Compute max Hamming distance
    max_hamming = 0
    for i in range(len(sorted_keys)):
        for j in range(i, len(sorted_keys)):
            s1 = filtered_seqs[sorted_keys[i]]
            s2 = filtered_seqs[sorted_keys[j]]
            dist = sum(1 for a, b in zip(s1, s2) if a != b)
            if dist > max_hamming:
                max_hamming = dist

    assert data["max_hamming_distance"] == max_hamming, \
        f"Incorrect max_hamming_distance. Expected {max_hamming}, got {data['max_hamming_distance']}."

    # Validate types of statistical results
    assert isinstance(data["top_singular_value"], float), "top_singular_value must be a float."
    assert isinstance(data["t_statistic"], float), "t_statistic must be a float."
    assert isinstance(data["p_value"], float), "p_value must be a float."