You are an MLOps engineer tasked with tracking experiment artifacts. A pipeline script located at `/home/user/analyze_artifacts.py` is failing and producing incorrect results. It is designed to analyze 50-dimensional model embeddings, but it currently suffers from a numerical library configuration error, a mathematical bug in its dimensionality reduction, and missing statistical features.

The script is supposed to:
1. Load 50-dimensional embeddings for Model A and Model B from `/home/user/embeddings.npz`.
2. Perform Principal Component Analysis (PCA) from scratch using Singular Value Decomposition (SVD) to reduce the data to 2 dimensions.
3. Save a scatter plot of the 2D embeddings to `/home/user/pca_plot.png`.
4. Compute the Euclidean distance between the centroids of Model A and Model B in the 2D PCA space, saving the scalar value to `/home/user/centroid_distance.txt` (rounded to 4 decimal places).
5. Perform an independent 2-sample t-test (assuming equal variances) on the FIRST principal component (PC1) between Model A and Model B to check if their distributions significantly differ. Save the resulting p-value to `/home/user/p_value.txt` (formatted in scientific notation with 4 decimal places, e.g., `1.2345e-04`).

Currently, the script has the following issues:
- It crashes in our headless CI/CD Linux environment due to a Matplotlib backend misconfiguration.
- The manual PCA implementation via SVD is mathematically incorrect because it forgets a crucial data preprocessing step fundamental to linear algebra.
- It is missing the code to compute the centroid distance and the hypothesis test.

Your task:
Fix the script `/home/user/analyze_artifacts.py` and run it successfully so that it outputs the correct `pca_plot.png`, `centroid_distance.txt`, and `p_value.txt`. 

Note: Do not use `sklearn` for the PCA; you must fix the existing `numpy` SVD implementation. PC1 is defined as the component with the largest variance.