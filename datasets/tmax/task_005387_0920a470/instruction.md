You are a performance engineer profiling a scientific application. The program `/home/user/fit_data.c` is designed to perform a 12th-degree polynomial regression on a dataset stored in an HDF5 file (`/home/user/data.h5`). 

However, the application crashes or produces wild, nonsensical results because the generated Vandermonde matrix leads to a near-singular normal matrix ($X^T X$), causing the LU decomposition to fail.

Your tasks are:
1. Modify `/home/user/fit_data.c` to implement Ridge Regression (Tikhonov regularization). Specifically, locate the `TODO` comment and add $\lambda = 0.001$ to the diagonal elements of the matrix $A$ before it is solved.
2. Compile the C program from source. You will need to link against the HDF5 and GSL (GNU Scientific Library) libraries, as well as the standard math library. Name the compiled executable `fit_data`.
3. Run the compiled executable and redirect its standard output to `/home/user/coeffs.txt`.

Ensure your final coefficients are printed one per line, matching the exact format the C code natively outputs.