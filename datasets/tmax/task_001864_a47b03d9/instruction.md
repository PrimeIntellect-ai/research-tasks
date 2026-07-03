You are helping a machine learning engineer prepare a dataset for training a PDE surrogate model. The raw dataset contains 1D spatial signals, but the numerical solver occasionally produced unstable, oscillating solutions that need to be filtered out before training.

The raw data is located at `/home/user/raw_signals.npy`. It is a 2D NumPy array of shape `(N, M)`, where `N` is the number of samples and `M` is the number of spatial points. The spatial domain is $x \in [0, 1]$, evenly spaced, meaning the grid spacing is $dx = 1.0 / (M - 1)$.

Your task is to write and execute a Python script (`/home/user/prepare_data.py`) that performs the following steps:
1. **Numerical Differentiation & Validation**: Calculate the discrete second derivative of each signal with respect to $x$. Use standard second-order finite differences (you can just use `numpy.diff(signal, n=2) / (dx**2)` which computes it for the interior points). Keep only the signals where the maximum absolute value of the second derivative is strictly less than `100.0`.
2. **Save Filtered Data**: Save the retained valid signals to a new file `/home/user/filtered_signals.npy` in the exact same format (2D array).
3. **Matrix Decomposition**: To ensure the filtered dataset has sufficient variance for training, perform a Singular Value Decomposition (SVD) on the filtered data matrix.
4. **Regression Logging**: Extract the top 3 largest singular values from the SVD and write them to `/home/user/report.txt`. The file should contain exactly one line with the 3 values formatted to 4 decimal places, separated by commas (e.g., `12.3456, 9.8765, 4.3210`).

Write the script, run it, and verify the outputs are created successfully.