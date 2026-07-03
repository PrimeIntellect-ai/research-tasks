You are a data scientist troubleshooting a floating-point instability issue in a statistical modeling pipeline. 

Your team uses C for high-performance data processing. However, a recent attempt to perform polynomial regression using the Normal Equations ($X^T X c = X^T y$) and LU decomposition yielded completely incorrect results due to catastrophic cancellation and the high condition number of the Vandermonde matrix.

Your task is to implement a numerically stable approach using Singular Value Decomposition (SVD).

We have placed an experimental dataset in HDF5 format at `/home/user/data.h5`. It contains two 1D datasets of `double` (float64) values: `/x` and `/y`, each of length 50.

Requirements:
1. Write a C program at `/home/user/fit_model.c` that reads the `/x` and `/y` datasets from `/home/user/data.h5`.
2. Construct a design matrix $X$ for a cubic polynomial fit (degree 3): $y = c_0 + c_1 x + c_2 x^2 + c_3 x^3$.
3. Use the GNU Scientific Library (GSL) to solve the overdetermined system $X c = y$ using its SVD-based linear multifit functions (e.g., `gsl_multifit_linear`). Do NOT form $X^T X$.
4. Output the 4 fitted coefficients ($c_0, c_1, c_2, c_3$) to `/home/user/coeffs.txt`, one per line, formatted to 6 decimal places (e.g., `%.6f`).
5. Compile and run your program. You will need to install the necessary HDF5 and GSL development headers and libraries. 
6. Create a script (Python or gnuplot) to visualize the original data points (scatter) and the fitted cubic curve (line). Save the plot as `/home/user/fit.png`.

The automated test will verify the presence and numerical accuracy of `/home/user/coeffs.txt` and the existence of `/home/user/fit.png`.