You are a Performance Engineer tasked with profiling application response times to filter out anomalous behaviors (e.g., memory leaks, network throttling) using statistical signal processing.

We have exported latency histograms from various server nodes. Some profiles reflect healthy baselines, while others exhibit anomalous latency spikes. You need to build a classifier to distinguish them.

**Step 1: Extract the Tolerance Specification**
You have been provided with an architecture specification image at `/app/profile_spec.png`. Use an OCR tool (like `tesseract`) to extract the text from this image. It contains a critical configuration string formatted like `THRESHOLD: X.XX`, which represents the maximum allowable probability distribution distance from our ideal baseline.

**Step 2: Build the Classifier**
Write a Python script at `/home/user/profile_classifier.py` that classifies a given latency profile CSV file. 
The script must be invoked as:
`python /home/user/profile_classifier.py <path_to_csv>`

Each CSV file contains two columns: `latency_ms` and `counts`.
Your script must perform the following reproducible computation pipeline:
1. Load the CSV.
2. Apply a Savitzky-Golay filter (`scipy.signal.savgol_filter`) to the `counts` array to smooth out sampling noise. Use `window_length=11` and `polyorder=3`. Ensure any negative values post-smoothing are clipped to 0.
3. Normalize the smoothed counts using numerical integration (trapezoidal rule via `numpy.trapz` or `scipy.integrate.trapezoid` over the `latency_ms` grid) so that the area under the curve is exactly 1.0. This yields the Empirical Probability Density Function (PDF).
4. Our baseline ideal performance is modeled as a Normal distribution with $\mu = 120.0$ and $\sigma = 20.0$. Calculate the ideal PDF over the same `latency_ms` grid.
5. Compute the 1D Wasserstein distance between the Empirical PDF and the Ideal PDF. *Note: Use `scipy.stats.wasserstein_distance` utilizing the normalized densities as weights, or compute it via inverse CDFs.*
6. If the calculated Wasserstein distance is strictly greater than the threshold extracted from the image, the script must exit with status code `1` (Reject / Anomalous). If it is less than or equal to the threshold, exit with status code `0` (Accept / Normal).

Ensure your script is robust and prints any necessary debugging information to standard output (this will not affect the grading as long as the exit code is correct). You may install any required python packages.