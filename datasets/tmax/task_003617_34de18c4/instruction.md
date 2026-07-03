You are a performance engineer profiling a scientific simulation pipeline. The pipeline occasionally crashes during matrix factorization steps. You suspect that the crashes are caused by near-singular input matrices. 

You need to analyze the matrices stored in an HDF5 dataset to identify the problematic inputs and estimate the probability density of the near-singular condition.

You have been provided with an HDF5 file at `/home/user/input_data.h5`. It contains a single dataset named `matrices` of shape (100, 50, 50) representing 100 matrices of size 50x50.

Your task is to:
1. Create a Python virtual environment at `/home/user/venv` and install any necessary scientific computing libraries.
2. Write a script to read the dataset and calculate the condition number of each matrix (using the 2-norm).
3. Identify all matrices with a condition number greater than or equal to $10^{12}$. Write their 0-based indices to `/home/user/singular_indices.txt`, with one integer index per line, sorted in ascending order.
4. Calculate the base-10 logarithm (`log10`) of all 100 condition numbers.
5. Perform a Gaussian Kernel Density Estimation (KDE) on these log10 condition numbers using standard Scott's Rule for bandwidth selection (as implemented by default in `scipy.stats.gaussian_kde`).
6. Evaluate the KDE probability density function at the value `12.0` (representing a condition number of $10^{12}$). Save this single density value, rounded to exactly 4 decimal places, to `/home/user/kde_result.txt`.

Ensure your environment is set up properly and all required outputs are written to the specified files.