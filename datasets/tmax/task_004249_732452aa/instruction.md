You are a data scientist working on an embedded systems project where Python is not available. You need to fit a cubic polynomial model $y = \beta_0 + \beta_1 x + \beta_2 x^2 + \beta_3 x^3$ to a set of observational data.

The observational data is provided in a single-line CSV file at `/home/user/data.csv`. The file contains flattened, interleaved coordinates in the format `x0,y0,x1,y1,x2,y2,...`.

Your task is to:
1. Write a C program at `/home/user/fit.c`.
2. The program must read and reshape the data from `/home/user/data.csv` into $x$ and $y$ vectors.
3. Construct the corresponding Vandermonde matrix and solve the least squares regression problem to find the coefficients $\beta_0, \beta_1, \beta_2, \beta_3$. You must use matrix decomposition (e.g., QR, LU, Cholesky, or SVD) to solve the system. You are allowed and encouraged to install and use a library like GSL (GNU Scientific Library) or LAPACKE (e.g., via `apt-get install -y libgsl-dev`).
4. The program must output the fitted coefficients to a file `/home/user/coefficients.txt` in the exact format: `%.4f,%.4f,%.4f,%.4f\n` representing $\beta_0, \beta_1, \beta_2, \beta_3$.

Compile and run your C program so that `/home/user/coefficients.txt` is generated with the correct values. Do not use Python or other high-level languages to perform the math.