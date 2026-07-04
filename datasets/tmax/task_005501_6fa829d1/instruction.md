You are a machine learning engineer preparing spectral training data for a new model. The raw data is noisy and high-dimensional. You need to denoise it using matrix decomposition and analyze the residuals to understand the noise distribution.

You have been provided with a dataset at `/home/user/spectra.csv`. It contains 100 rows (samples) and 50 columns (wavelength features) of comma-separated float values, with no header.

Write a Go program at `/home/user/process.go` that performs the following steps:
1. Parse the CSV file into a 100x50 matrix.
2. Center the data: for each of the 50 columns, compute its mean and subtract it from every element in that column. Let this be the centered matrix `X`.
3. Perform Singular Value Decomposition (SVD) on `X`.
4. Perform convergence testing to find `k`: the minimum number of top singular values required such that the sum of their squares is at least 95% (0.95) of the sum of squares of all singular values.
5. Reconstruct the denoised matrix `X_k` using only the top `k` singular values and their corresponding vectors.
6. Calculate the residual matrix `R = X - X_k`.
7. Perform distribution fitting on the noise: calculate the mean and standard deviation of all 5000 elements in the residual matrix `R`. (Use the population standard deviation formula, dividing by N=5000).
8. Output a JSON file at `/home/user/results.json` with the following structure:
```json
{
  "k": <integer>,
  "residual_mean": <float>,
  "residual_std": <float>
}
```

You must initialize a Go module in `/home/user` and you may use third-party libraries like `gonum.org/v1/gonum/mat` to perform the matrix operations. Once your program is written, compile and run it to produce `/home/user/results.json`.

Ensure your Go code is mathematically correct and handles the standard deviation of the flattened residual matrix.