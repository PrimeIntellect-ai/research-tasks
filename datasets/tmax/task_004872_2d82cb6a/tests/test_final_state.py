# test_final_state.py
import os
import numpy as np
import pytest

def test_weights_file_exists():
    assert os.path.isfile('/home/user/weights.csv'), "The file /home/user/weights.csv is missing."

def test_package_fixed_and_mse_threshold():
    # Attempt to import and use the fixed package
    try:
        from dna_factorize import embed_sequences
    except ImportError:
        pytest.fail("Could not import `dna_factorize`. Was the fixed package installed?")

    primers_path = '/home/user/primers.txt'
    assert os.path.isfile(primers_path), f"Missing {primers_path}"

    with open(primers_path) as f:
        primers = [line.strip() for line in f if line.strip()]

    try:
        embeddings = embed_sequences(primers)
    except Exception as e:
        pytest.fail(f"embed_sequences failed with error: {e}. Is the NaN bug fixed?")

    assert not np.isnan(embeddings).any(), "Embeddings contain NaNs. The division-by-zero bug in dna_factorize/core.py is not properly fixed."
    assert embeddings.shape == (100, 16), f"Expected embeddings shape (100, 16), got {embeddings.shape}"

    weights_path = '/home/user/weights.csv'
    try:
        weights = np.loadtxt(weights_path, delimiter=',')
    except Exception as e:
        pytest.fail(f"Could not load weights from {weights_path}: {e}")

    assert weights.shape == (100,), f"Expected 100 weights in {weights_path}, got shape {weights.shape}"

    # Enforce sum to 1 for evaluation
    weights_sum = np.sum(weights)
    assert weights_sum > 0, "Sum of weights must be greater than 0"
    weights = weights / weights_sum

    pred = np.average(embeddings, axis=0, weights=weights)

    target_path = '/home/user/target_profile.npy'
    assert os.path.isfile(target_path), f"Missing {target_path}"
    target = np.load(target_path)

    mse = np.mean((pred - target)**2)
    threshold = 0.005

    assert mse <= threshold, f"MSE {mse:.6f} is greater than the threshold {threshold}. The optimized weights do not match the target profile closely enough."