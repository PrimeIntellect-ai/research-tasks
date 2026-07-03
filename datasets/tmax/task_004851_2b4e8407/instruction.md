You are acting as a machine learning engineer preparing a dataset for a downstream modeling task. You have received a dataset of high-dimensional continuous features, but you suspect it contains a lot of redundant information and want to reduce its dimensionality while ensuring the marginal distributions of the features aren't drastically altered.

You have been provided with a NumPy array file at `/home/user/features.npy`. This file contains a 2D matrix representing our dataset (rows are samples, columns are features).

Please perform the following steps:
1. Load the dataset using Python.
2. Perform Singular Value Decomposition (SVD) on the matrix. Note: Use the data as-is (do not mean-center or scale it before SVD for this specific task).
3. Determine the minimum number of principal components ($k$) required to retain at least 95.0% of the total variance. (Calculate the variance explained by each component as the square of its singular value divided by the sum of all squared singular values).
4. Reconstruct the dataset back to its original dimensions using only these top $k$ components. Let's call this reconstructed matrix `X_hat`.
5. To check if the reconstruction preserves the distribution of the individual features, perform a two-sample Kolmogorov-Smirnov (KS) test comparing the first feature (column index `0`) of the original dataset against the first feature (column index `0`) of the reconstructed dataset `X_hat`.
6. Write your results to a file located at `/home/user/report.txt` exactly in the following format:
   - Line 1: The integer value of $k$.
   - Line 2: The p-value from the KS test, rounded to exactly 4 decimal places.

Ensure you create the final text file precisely as requested.