You are a data scientist tasked with fitting a harmonic model to high-frequency sensor data. You need to identify the dominant frequencies in the signal, construct a basis, and fit a linear model using matrix decomposition. To handle processing efficiently, the fitting must be parallelized across data chunks.

There is a dataset located at `/home/user/sensor_data.csv` with two columns: `t` (time in seconds) and `y` (signal amplitude).

Write and execute a Python script at `/home/user/fit_model.py` that performs the following steps:
1. Load the CSV data.
2. Use Fourier Transform (`numpy.fft` or `scipy.fft`) on the *entire* signal `y` to identify the top 2 dominant positive, non-zero frequencies (in Hz). Assume the time steps are evenly spaced.
3. Split the data (`t` and `y`) into 4 equal, sequential chunks (e.g., if there are 1000 rows, chunk 0 is rows 0-249, chunk 1 is 250-499, etc.).
4. Write a function `fit_chunk(t_chunk, y_chunk, freqs)` that:
    - Constructs a design matrix $X$ for the given time chunk using the two dominant frequencies $f_1$ and $f_2$ (sorted in ascending order). The columns of $X$ must be exactly in this order: $[1, \cos(2\pi f_1 t), \sin(2\pi f_1 t), \cos(2\pi f_2 t), \sin(2\pi f_2 t)]$.
    - Solves for the coefficient vector $\beta$ (least squares) manually using Singular Value Decomposition (SVD) via `numpy.linalg.svd`. Do **not** use `numpy.linalg.lstsq` or `scikit-learn`. Use the Moore-Penrose pseudoinverse logic: $\beta = V^T \Sigma^{-1} U^T y$.
5. Use Python's `concurrent.futures.ProcessPoolExecutor` (or `multiprocessing.Pool`) to run `fit_chunk` on all 4 chunks in parallel.
6. Save the results of the exact extracted frequencies and the weights from the *first* chunk (chunk 0) into a JSON file at `/home/user/model_results.json` in the following format:
```json
{
  "frequencies": [f1, f2],
  "weights_chunk_0": [b0, b1, b2, b3, b4]
}
```
Round the frequencies to 2 decimal places, and each weight in the array to 3 decimal places.