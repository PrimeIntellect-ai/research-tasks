You are a Machine Learning Engineer tasked with preparing a training data pipeline for a new acoustic classification model. The raw signals suffer from non-linear frequency distortions, and you need to build a robust preprocessing server that cleans and extracts features from these signals in real-time.

Your pipeline involves a custom, proprietary package `freq_optimizer-1.0` (vendored at `/app/freq_optimizer-1.0`). However, the previous engineer left it in a broken state. You must fix it, integrate it with a spectral analysis and optimization script, and expose the results via a dual-protocol server.

Here are your specific requirements:

**Phase 1: Fix and Install the Vendored Package**
1. Navigate to `/app/freq_optimizer-1.0`. This package contains a C-extension for fast numerical processing. 
2. The package currently fails to compile or produces unresolved symbols when imported because its `Makefile` (which is invoked by `setup.py`) is missing the flag to link the standard math library. Identify the `Makefile`, fix the missing link flag, and install the package globally via `pip install .`.
3. To verify numerical stability, the package must be able to process arrays containing zeros and large numbers without throwing `NaN` or `OverflowError` during its internal exponential decay calculations.

**Phase 2: Signal Processing and Optimization**
Create a Python module that performs the following on an input array of floats (a time-domain signal):
1. Use `freq_optimizer.denoise(signal)` to remove high-frequency artifacts. 
2. Compute the 1D discrete Fourier Transform (FFT) of the denoised signal using `numpy.fft.fft`. Keep only the real magnitudes of the positive frequencies.
3. You must fit a smoothing curve to these magnitudes. Use `scipy.optimize.minimize` (with the Nelder-Mead simplex algorithm) to find a scalar parameter `alpha` (starting guess `alpha=1.0`) that minimizes the Mean Squared Error (MSE) between the extracted magnitudes and a target exponential decay function: `target[i] = 100 * exp(-alpha * i)`.
4. The output of your processing pipeline for a given signal should be the optimized `alpha` value and the smoothed array (i.e., `100 * exp(-alpha * i)` for `i` in range of the magnitude array length).

**Phase 3: Multi-Protocol Serving**
You must expose your preprocessing pipeline via a long-running server. The server must bind to two interfaces simultaneously:
1. **HTTP API**: Listen on `127.0.0.1:8000`.
   - Endpoint: `POST /process`
   - Header Required: `Authorization: Bearer ML_SECRET_2024`
   - Request Body: JSON format `{"signal": [float, float, ...]}`
   - Response Body: JSON format `{"alpha": float, "smoothed_spectrum": [float, float, ...]}`
2. **TCP Socket API**: Listen on `127.0.0.1:9000`.
   - The connection must first accept a single newline-terminated line: `AUTH:ML_SECRET_2024\n`. If the auth is incorrect, close the connection.
   - Subsequent lines will be comma-separated floats representing the signal (e.g., `1.0,-0.5,0.2\n`).
   - The server must respond with comma-separated floats of the `smoothed_spectrum` followed by a newline.

Write and start this server. Leave it running in the background. Do not exit the server process.

Write your code in `/home/user/pipeline_server.py` and run it. The automated test will connect to ports 8000 and 9000 to verify your service.