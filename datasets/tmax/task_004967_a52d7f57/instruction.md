You are acting as a bioinformatics analyst. We are trying to perform novelty detection on DNA sequences based on their k-mer profiles. 

In `/home/user/`, you will find two numpy arrays:
- `kmer_cov.npy`: A 50x50 covariance matrix of k-mer frequencies from a background dataset.
- `kmer_diffs.npy`: A 1000x50 matrix where each row represents the difference between a new sequence's k-mer profile and the background mean.

We originally tried to compute the Mahalanobis distance for each sequence using the Cholesky decomposition of the covariance matrix. However, because DNA sequences often contain highly repetitive elements, the k-mer covariance matrix is rank-deficient (near-singular), causing the standard Cholesky-based inverse to fail with a `LinAlgError`.

Your task is to implement a robust pipeline from scratch:
1. Load the matrices from `/home/user/kmer_cov.npy` and `/home/user/kmer_diffs.npy`.
2. Compute the Moore-Penrose pseudo-inverse of the covariance matrix using Singular Value Decomposition (SVD). When computing the pseudo-inverse, strictly zero out any singular values that are less than `1e-10`.
3. Compute the robust Mahalanobis distance for each sequence difference vector $x_i$. The distance is defined as $D_i = \sqrt{x_i \Sigma^+ x_i^T}$, where $\Sigma^+$ is your pseudo-inverse.
4. To establish an anomaly threshold for novel sequences, fit a Gamma distribution to the resulting array of 1000 distances using `scipy.stats.gamma.fit`. **Important:** Fix the location parameter to 0 by passing `floc=0` to the fit function to ensure stability and comparability.
5. Calculate the 95th percentile (CDF = 0.95) of this fitted Gamma distribution.
6. Write the final 95th percentile threshold, rounded to exactly 4 decimal places, to a file located at `/home/user/anomaly_threshold.txt`.