A researcher in our lab has been building a distributed pipeline for analyzing spectral signals from noisy spectroscopy detectors. However, we are encountering a major issue: the pipeline occasionally produces non-reproducible, non-deterministic results when computing total spectral energies and spectral moments across different worker nodes. We suspect this is due to floating-point reduction order issues (e.g., standard `sum()` accumulating rounding errors differently depending on chunking).

Your task is to fix the distributed setup and rewrite the core signal processing script to be bit-exact and reproducible.

The system relies on three services located in `/app/`:
1. **Redis**: Used for caching results (runs on port 6379).
2. **Flask API**: Located in `/app/api/`. It receives signal data, caches it in Redis, and calls the processing script. (Runs on port 5000).
3. **Nginx**: Should act as a reverse proxy on port 8080, routing requests to `/api/` to the Flask app.

**Part 1: Service Composition**
- The nginx configuration at `/app/nginx/nginx.conf` is missing the routing for the Flask app. Edit it so that any request to `http://127.0.0.1:8080/api/...` is proxied to `http://127.0.0.1:5000/...`.
- Start Redis, the Flask API (using `python3 /app/api/app.py`), and Nginx.

**Part 2: The Signal Processing Script**
Rewrite the processing script at `/home/user/process_signal.py`. 
It must accept exactly one command-line argument: the path to a JSON file containing an array of floats (the time-domain signal).
The script must perform the following steps exactly, in order:
1. Load the JSON array of floats. Let the length be $N$.
2. Apply a standard Hanning window to the signal. (Use exactly $w[n] = 0.5 - 0.5 \cos(\frac{2\pi n}{N-1})$).
3. Compute the Real Fast Fourier Transform (Real FFT) using `numpy.fft.rfft`.
4. Calculate the power spectrum: $P[k] = |X[k]|^2$.
5. To guarantee reproducibility and eliminate floating-point reduction order variance, calculate the `total_energy` (sum of $P$) and the `weighted_centroid` ($\sum (k \cdot P[k]) / \text{total\_energy}$) using Python's `math.fsum()`. Do NOT use `numpy.sum()` or standard `+` loops for the final accumulation of these two values, as they do not provide strict IEEE-754 precision tracking for arbitrary orders.
6. Print a valid JSON object to `stdout` with exactly these keys:
   `{"total_energy": <float>, "weighted_centroid": <float>, "peak_index": <int>}`
   Where `peak_index` is the integer index of the maximum value in the power spectrum.

We have a pre-compiled oracle binary that correctly implements this strict-reduction arithmetic. Our CI pipeline will randomly generate thousands of signals and assert that your `process_signal.py` matches the oracle's output bit-for-bit, and will test the end-to-end API via Nginx.