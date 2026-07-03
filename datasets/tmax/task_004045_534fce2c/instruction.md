I am trying to fit a linear model $Ax = b$ on a dataset, but the matrix $A$ is near-singular due to highly collinear features. Ordinary least squares is failing by producing completely unstable, massive coefficients.

The data is stored in an HDF5 file located at `/home/user/input.h5` with the following datasets:
- `A`: A 2D numpy array (the design matrix).
- `b`: A 1D numpy array (the target vector).

I need you to write and execute a Python script that does the following:
1. Reads the matrix `A` and vector `b` from `/home/user/input.h5`.
2. Computes the Ridge regression estimate for $x$ using a regularization parameter $\lambda = 10^{-4}$. The formula for Ridge regression is $x = (A^T A + \lambda I)^{-1} A^T b$, where $I$ is the identity matrix.
3. Saves the resulting vector $x$ as an HDF5 dataset named `x_ridge` inside a new file `/home/user/output.h5`.
4. Calculates the L2 norm (Euclidean norm) of the vector $x_ridge$, rounded to 4 decimal places, and writes this single floating-point number to a text file at `/home/user/norm.log`.

Ensure your calculations are precise and that you handle the HDF5 I/O properly.