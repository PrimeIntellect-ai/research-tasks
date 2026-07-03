I am preparing a synthetic training dataset for a machine learning model, and I need a C program to inject specific correlations into my raw Monte Carlo noise samples.

I have a file at `/home/user/raw_noise.csv` containing 1000 rows of uncorrelated standard normal variables. The file has no header, and each row contains 3 comma-separated floating-point values ($z_1, z_2, z_3$).

I need you to write and execute a C program at `/home/user/augment.c` that does the following:
1. Hardcodes the following 3x3 target Covariance Matrix ($C$):
   1.0, 0.5, 0.2
   0.5, 1.0, 0.3
   0.2, 0.3, 1.0
2. Computes the Cholesky decomposition of this matrix to find the lower triangular matrix $L$ (such that $C = L L^T$).
3. Reads the uncorrelated samples $Z = [z_1, z_2, z_3]^T$ from `/home/user/raw_noise.csv`.
4. Transforms each sample into a correlated sample $X = [x_1, x_2, x_3]^T$ using the matrix multiplication $X = L Z$.
5. Outputs the reshaped and correlated data to `/home/user/correlated_features.csv`.

The output file `/home/user/correlated_features.csv` must include a header `id,f1,f2,f3` and format the floating-point numbers to exactly 4 decimal places (e.g., `%.4f`). The `id` should be an integer starting from 0.

Write the code, compile it (don't forget to link the math library if needed), and run it so the output file is generated.