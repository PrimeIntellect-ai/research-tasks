You are a performance engineer profiling a spectroscopy analysis application. The application processes high-resolution signal data using Non-negative Matrix Factorization (NMF) to extract underlying spectral components. However, the input spectra are highly correlated (near-singular), causing the NMF algorithm to struggle with convergence, often hitting the maximum iteration limit. 

Your task is to implement a preprocessing step using a provided C library, and then perform a convergence test to find the minimum regularization parameter required for the NMF to converge efficiently.

Follow these steps:

1. **Environment Setup**: Ensure `numpy` and `scikit-learn` are installed in your Python environment.
2. **Compile Preprocessing Routine**: You have been provided with a C file at `/home/user/smooth.c`. It contains a simple 3-point moving average function `void smooth(double* input, double* output, int n)`. Compile this file into a shared library named `/home/user/libsmooth.so`.
3. **Data Processing Script**: Write a Python script at `/home/user/analyze.py` that does the following:
   - Loads the spectroscopy data from `/home/user/spectra.csv` (a 2D matrix where each row is a spectrum).
   - Uses the `ctypes` module to load `/home/user/libsmooth.so` and applies the `smooth` C function to *each row* of the loaded data, storing the result in a new smoothed data array of the same shape.
   - Performs a convergence test on the smoothed data using `sklearn.decomposition.NMF`. Use the following fixed parameters: `n_components=2`, `init='random'`, `random_state=42`, `max_iter=500`, `solver='cd'`, `l1_ratio=1.0`.
   - Iterate a regularization parameter `alpha` from `0.0` to `1.0` in increments of `0.1` (i.e., `0.0`, `0.1`, `0.2`, ..., `1.0`). For each `alpha`, set both `alpha_W=alpha` and `alpha_H=alpha` in the NMF constructor, and fit the model on the smoothed data.
   - Find the smallest `alpha` (checking in ascending order) for which the NMF converges (meaning the number of iterations `nmf.n_iter_` is strictly less than `max_iter`, which is 500).
4. **Output Results**: Once the minimum converging `alpha` is found, write it and the number of iterations it took to a file at `/home/user/result.txt` exactly in this format: `alpha=X.X, iter=Y` (e.g., `alpha=0.3, iter=124`). Stop testing higher `alpha` values once convergence is found.

Note: The data file `/home/user/spectra.csv` and the C file `/home/user/smooth.c` already exist in your workspace.