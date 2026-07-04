You are a data scientist tasked with building a reproducible data processing and model-fitting pipeline. You need to process noisy spatio-temporal sensor data, extract the main patterns, and fit a linear model to a target variable. 

You have two input files:
1. `/home/user/signals.csv`: A matrix of 1000 rows (time steps) and 50 columns (sensors). No headers.
2. `/home/user/target.csv`: A single column of 1000 rows (target values). No headers.

Please write and execute a Python script that performs the following deterministic pipeline:

**Phase 1: Spectral Filtering (FFT)**
- Load `/home/user/signals.csv` into a NumPy array.
- For each of the 50 sensor columns, apply a 1D Discrete Fourier Transform (`numpy.fft.fft`).
- Calculate the sample frequencies using `numpy.fft.fftfreq(1000)`.
- Zero out the complex Fourier coefficients for any frequency `f` where the absolute value `abs(f) > 0.1` (this acts as a low-pass filter).
- Reconstruct the filtered signals using the inverse FFT (`numpy.fft.ifft`) and take the real part. 

**Phase 2: Dimensionality Reduction (Matrix Decomposition)**
- Let the filtered data matrix be $X$ (1000 x 50).
- Perform Singular Value Decomposition (SVD) on $X$ such that $X = U \Sigma V^T$. Use `numpy.linalg.svd(X, full_matrices=False)`.
- Extract the top 3 components. Create the feature matrix $F$ (1000 x 3) by taking the first 3 columns of $U$ and multiplying by the 3x3 diagonal submatrix of $\Sigma$. Equivalently, $F = X \cdot V^T[:, :3]$.

**Phase 3: Model Fitting**
- Load `/home/user/target.csv` as a 1D array $y$ (length 1000).
- Fit a linear regression model to predict $y$ from $F$ without an intercept. Use `numpy.linalg.lstsq(F, y, rcond=None)` to find the weights $w$.

**Phase 4: Output**
- Save the 3 resulting weights to `/home/user/weights.txt`. 
- The file should contain a single line with the 3 weights separated by commas, formatted to exactly 6 decimal places (e.g., `1.234567,-0.123456,9.876543`).

Ensure your environment has the necessary libraries (e.g., install `numpy` if missing using `pip`). You must complete the task by generating the final `/home/user/weights.txt` file.