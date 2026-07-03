You are acting as a performance engineer assisting with a numerical profiling task. One of our legacy applications attempts to fit a high-degree polynomial to sensor data, but the naive normal equations approach ($X^T X \beta = X^T y$) is failing due to a near-singular, ill-conditioned matrix. 

Your task is to implement a numerically stable polynomial regression and validate it.

1. Read the input data from an HDF5 file located at `/home/user/signal.h5`. It contains two datasets: `t` (time) and `signal` (observed values).
2. Write a Python script `/home/user/stable_fit.py` that fits a degree-12 polynomial to this data. You must use a numerically stable method (like SVD-based least squares) rather than explicitly computing the inverse of $X^T X$.
3. Save the resulting polynomial coefficients (ordered from highest degree to 0th degree) to `/home/user/coeffs.txt`, with one coefficient per line formatted to 8 decimal places.
4. Validate your solution by computing the Mean Squared Error (MSE) between the fitted polynomial values and the original `signal` data. Save this single MSE value to `/home/user/mse.txt`, formatted to 8 decimal places.

Ensure your code handles the scientific data formats correctly and overcomes the matrix factorization instability natively.