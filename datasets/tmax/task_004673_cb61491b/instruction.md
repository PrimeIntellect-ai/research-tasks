You are assisting a researcher who is analyzing snapshots of a fluid dynamics simulation.

The simulated 2D velocity field is stored as a 100x50 double-precision floating-point matrix in an HDF5 file located at `/home/user/sim_matrix.h5` under the dataset name `matrix_data`.

The researcher needs you to extract the dominant spatial modes using Singular Value Decomposition (SVD) and compare them to a reference baseline.

Write a C program (save it as `/home/user/analyze.c`) that performs the following steps:
1. Reads the `matrix_data` (100 rows, 50 columns) from the HDF5 file `/home/user/sim_matrix.h5`.
2. Computes the Singular Value Decomposition (SVD) of this matrix. You must use the GNU Scientific Library (GSL) for the matrix decomposition.
3. Extracts the top 3 largest singular values.
4. Writes these 3 singular values to a text file at `/home/user/top_sv.txt`, one value per line, formatted to 6 decimal places (`%.6f`).
5. Reads the 3 reference singular values from the text file `/home/user/reference_sv.txt` (which already exists).
6. Computes the Mean Absolute Error (MAE) between your computed top 3 singular values and the reference values.
7. Writes this single MAE value to `/home/user/sv_error.txt`, formatted to 6 decimal places (`%.6f`).

Compile and run your C code. You are allowed to use standard Linux tools and write bash scripts to aid your compilation if needed. Make sure to link against the necessary HDF5 and GSL libraries.