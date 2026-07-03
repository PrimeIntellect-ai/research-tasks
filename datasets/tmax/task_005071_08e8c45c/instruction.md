You are a machine learning engineer preparing a data processing pipeline. As part of a dimensionality reduction step, we need to evaluate the variance explained by the principal components of our dataset to ensure reproducibility and numerical accuracy. 

Our primary backend language is Go.

You have been provided a dataset at `/home/user/data/features.csv`. It contains rows of floating-point numbers separated by commas (no header).

Your task is to:
1. Initialize a Go module named `mle/variance` in `/home/user/src`.
2. Install the Gonum numerical library (`gonum.org/v1/gonum`).
3. Write a Go program at `/home/user/src/main.go` that does the following:
   a. Reads the dataset from `/home/user/data/features.csv`.
   b. Centers the dataset (subtract the mean of each column from every value in that column).
   c. Computes the sample covariance matrix of the centered data (using N-1 for degrees of freedom).
   d. Computes the eigenvalues of the covariance matrix.
   e. Sorts the eigenvalues in descending order.
   f. Writes the sorted eigenvalues to `/home/user/output/eigen.txt`, with each eigenvalue on a new line, formatted to exactly 4 decimal places (e.g., `12.3456`).

Constraints & Requirements:
- You must use the `gonum.org/v1/gonum/mat` and `gonum.org/v1/gonum/stat` (or standard `mat.Eigen`) packages for numerical computations.
- Do not use any external ML frameworks besides Gonum.
- Ensure the directories `/home/user/src` and `/home/user/output` are created if they do not exist.
- Run your program to generate `/home/user/output/eigen.txt`.