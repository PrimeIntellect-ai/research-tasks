You are a bioinformatics analyst studying gene expression modules. You have a dataset `/home/user/gene_expression.csv` containing a matrix of gene expression levels (50 samples as rows, 10 genes as columns). 

You are using an Alternating Least Squares (ALS) Non-negative Matrix Factorization (NMF) script to find modules. The base script is located at `/home/user/als_nmf.py`.

Currently, the script runs fine for `k=3` (rank 3), but crashes with a `numpy.linalg.LinAlgError: Singular matrix` (or extreme numerical instability) when you attempt to run it for `k=4`. This happens because the input data is near-singular (true rank is ~3), causing the internal matrices to become non-invertible during the least-squares update steps.

Your task is to fix the script, evaluate convergence, and statistically compare the `k=3` and `k=4` models.

Perform the following steps:
1. **Regularization:** Modify `als_nmf.py` to add L2 (Ridge) regularization to both the `H` and `W` update steps. Add `0.1 * np.eye(k)` to the square matrices being inverted/solved.
2. **Convergence Testing:** Modify the training loop to track the total sum of squared errors loss: `loss = np.sum((V - W @ H)**2)`. Stop the loop early if the absolute change in this loss from the previous iteration is strictly less than `1e-4`.
3. **Visualization:** Run your modified ALS NMF algorithm for both `k=3` and `k=4`. Create a line plot showing the loss at each iteration for both models on the same figure. Save this plot to `/home/user/convergence.png`.
4. **Statistical Hypothesis Comparison:** After both models have converged, compute the final *per-sample* squared reconstruction error (summing over the 10 genes for each of the 50 samples, resulting in an array of 50 errors per model). Perform a paired Student's t-test (`scipy.stats.ttest_rel`) comparing the 50 per-sample errors of `k=3` against the 50 per-sample errors of `k=4`.
5. **Reporting:** Save a JSON file `/home/user/results.json` containing the following keys (all as floats):
   - `"k3_loss"`: The final total sum of squared errors for `k=3`.
   - `"k4_loss"`: The final total sum of squared errors for `k=4`.
   - `"p_value"`: The p-value from the paired t-test comparing the per-sample errors.

**Constraints & Details:**
- Keep the `np.random.seed(42)` initialization exactly as it is in the provided script so your results are deterministic.
- Do not use `sklearn.decomposition.NMF`; you must modify the provided `als_nmf.py` script.
- Ensure all required output files (`convergence.png`, `results.json`) are created in `/home/user/`.