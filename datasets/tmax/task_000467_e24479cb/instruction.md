You are a performance engineer profiling a high-frequency trading application. Your team has captured a raw telemetry trace containing the application's signal mixed with background system noise, alongside an ideal reference profile. You need to develop a diagnostic pipeline that isolates the application's signal, optimizes a filter, and serves the results via a local API.

You have been provided with two files:
1. `/app/trace_data.nc` (NetCDF format): Contains a time-series dimension `time` (length 10000) representing 10 seconds of data (sampling frequency = 1000 Hz). It has two datasets: `telemetry` (the raw, noisy profile) and `reference` (the ideal reference signal).
2. `/app/profiling_memo.wav`: An audio recording from the lead engineer containing the secure "baseline ID" required to authenticate your diagnostic service.

Perform the following workflow using Python:

**1. Data Normalization (Density Estimation)**
Read the `telemetry` and `reference` arrays. Normalize both arrays independently. To normalize an array, subtract its mode (the peak density value) and divide by its standard deviation. 
*Constraint:* Compute the mode by fitting a Gaussian Kernel Density Estimate (KDE) to the array's histogram (use a grid of 1000 points evenly spaced between the array's minimum and maximum values).

**2. Signal Optimization and Filtering**
Apply a 4th-order Butterworth bandpass filter to the normalized `telemetry` array. 
Using an optimization algorithm (e.g., Nelder-Mead simplex via `scipy.optimize.minimize`), find the optimal `low_cutoff` and `high_cutoff` frequencies (in Hz) that minimize the Mean Squared Error (MSE) between the filtered `telemetry` and the normalized `reference` array.
*Constraints:* 
- Use an initial guess of `low_cutoff = 40.0` and `high_cutoff = 200.0`. 
- Bound the optimization such that `10.0 <= low_cutoff <= 100.0` and `150.0 <= high_cutoff <= 400.0`.

**3. Scientific Output**
Save your final optimized, filtered telemetry array to an HDF5 file located at `/home/user/optimized_trace.h5` inside a dataset named `filtered_telemetry`.

**4. Telemetry Service (Multi-Protocol)**
Transcribe `/app/profiling_memo.wav` to discover the 4-digit Baseline ID. 
Write and start a background HTTP service (e.g., using Flask or FastAPI) listening on `127.0.0.1:8080`. 
The service must expose a POST endpoint at `/api/v1/profile`. It should accept a JSON payload. 
If the payload contains `{"auth": "<THE_4_DIGIT_BASELINE_ID>"}`, it must return an HTTP 200 response with the JSON payload:
`{"low_cutoff": <float>, "high_cutoff": <float>}` (round the frequencies to 2 decimal places).
If the authentication fails or is missing, return HTTP 403.

Keep the HTTP server running in the background so it can be verified.