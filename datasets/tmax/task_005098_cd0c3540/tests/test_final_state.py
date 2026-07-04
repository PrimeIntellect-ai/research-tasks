# test_final_state.py
import os
import math
import pytest

def test_pca_plot_exists():
    """Verify that the PCA plot was generated."""
    plot_path = '/home/user/pca_plot.png'
    assert os.path.exists(plot_path), f"File {plot_path} is missing. The script did not generate the plot."
    assert os.path.isfile(plot_path), f"Path {plot_path} is not a file."
    assert os.path.getsize(plot_path) > 0, f"File {plot_path} is empty."

def test_centroid_distance_correctness():
    """Verify that the centroid distance is calculated correctly and saved."""
    dist_path = '/home/user/centroid_distance.txt'
    assert os.path.exists(dist_path), f"File {dist_path} is missing."

    with open(dist_path, 'r') as f:
        content = f.read().strip()

    try:
        actual_dist = float(content)
    except ValueError:
        pytest.fail(f"Content of {dist_path} is not a valid float: '{content}'")

    # The expected distance is ~3.3087 based on the truth logic
    # We will compute it exactly from the npz to be robust
    import numpy as np
    data = np.load('/home/user/embeddings.npz')
    A, B = data['A'], data['B']
    X = np.vstack((A, B))
    X_centered = X - np.mean(X, axis=0)
    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
    X_pca = X_centered @ Vt.T[:, :2]
    A_pca, B_pca = X_pca[:len(A)], X_pca[len(A):]

    c_A = np.mean(A_pca, axis=0)
    c_B = np.mean(B_pca, axis=0)
    expected_dist = np.linalg.norm(c_A - c_B)

    assert math.isclose(actual_dist, expected_dist, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected centroid distance ~{expected_dist:.4f}, but got {actual_dist}. Did you mean-center the data before SVD?"

def test_p_value_correctness():
    """Verify that the p-value is calculated correctly and saved."""
    pval_path = '/home/user/p_value.txt'
    assert os.path.exists(pval_path), f"File {pval_path} is missing."

    with open(pval_path, 'r') as f:
        content = f.read().strip()

    try:
        actual_p = float(content)
    except ValueError:
        pytest.fail(f"Content of {pval_path} is not a valid float: '{content}'")

    import numpy as np
    from scipy import stats
    data = np.load('/home/user/embeddings.npz')
    A, B = data['A'], data['B']
    X = np.vstack((A, B))
    X_centered = X - np.mean(X, axis=0)
    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
    X_pca = X_centered @ Vt.T[:, :2]
    A_pca, B_pca = X_pca[:len(A)], X_pca[len(A):]

    _, expected_p = stats.ttest_ind(A_pca[:, 0], B_pca[:, 0])

    # SVD signs can be flipped, but t-test p-value is invariant to sign flips
    assert math.isclose(actual_p, expected_p, rel_tol=1e-2, abs_tol=1e-25), \
        f"Expected p-value ~{expected_p:.4e}, but got {actual_p:.4e}. Did you use PC1 and mean-center the data?"