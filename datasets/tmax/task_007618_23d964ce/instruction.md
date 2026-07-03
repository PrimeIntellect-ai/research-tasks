You are helping a data scientist debug and finalize a custom model fitting script. The current script `/home/user/fit_model.py` performs gradient descent to optimize a custom objective function on a synthetic dataset located at `/home/user/data/X.npy` and `/home/user/data/y.npy`. 

However, the script has three major issues:
1. **Numerical Instability**: The `compute_loss` and `compute_gradient` functions compute `np.exp(z)` directly. Because the features in `X.npy` are large, this causes catastrophic numerical overflow (`NaN` values). You need to rewrite these functions to be numerically stable. You may use `numpy` or `scipy.special` functions (like `logaddexp` or `expit`).
2. **Missing Convergence Testing**: The optimization loop runs for a fixed 10,000 iterations. Update the loop to include a convergence check: stop the optimization early if the absolute difference between the loss of the previous iteration and the current iteration is strictly less than `1e-5`.
3. **Lack of Reproducibility**: The initial weights `theta` are generated randomly, but no random seed is set. Ensure that `np.random.seed(42)` is called exactly once before generating the initial `theta` using `np.random.randn(X.shape[1])`.

The learning rate is already set to `0.001`. Do not change the learning rate.

Your task:
1. Fix the `fit_model.py` script as described above.
2. Run the script.
3. The script must save the final optimized weights as a NumPy array to `/home/user/theta.npy`.
4. The script must also save a JSON file at `/home/user/metrics.json` containing the exact number of iterations completed (integer) and the final loss value (float) in the format:
`{"iterations": <int>, "final_loss": <float>}`

Make sure you do not alter the way `X` and `y` are loaded, and ensure your fixed loss and gradient mathematically represent the same objective (binary cross-entropy without regularization).