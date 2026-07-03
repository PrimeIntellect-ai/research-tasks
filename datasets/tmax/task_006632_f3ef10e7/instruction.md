You are a performance engineer analyzing the latency logs of two versions of a backend microservice (V1 and V2). You suspect that V1 has a periodic latency spike caused by a misconfigured garbage collector, and you need to quantify the performance differences between the two versions.

You have been provided with two raw log files:
- `/home/user/v1_latency.csv`
- `/home/user/v2_latency.csv`

Each file has a header `timestamp,latency_ms` and contains data sampled at exactly 10 Hz (one sample every 0.1 seconds). Occasionally, some lines have the latency recorded as `TIMEOUT`.

Your task is to write a Bash script `/home/user/analyze.sh` that automates the data cleaning and statistical profiling pipeline. 

The pipeline must perform the following steps:
1. **Data Cleaning (Bash)**: Using standard shell utilities (e.g., `grep`, `awk`, `sed`), your Bash script must remove the header and any lines containing `TIMEOUT` from both CSV files. Save the cleaned data to temporary files.
2. **Statistical Analysis (Python)**: Your Bash script must invoke a Python script (which you must also write, e.g., `/home/user/stats.py`) that reads the cleaned data and calculates:
   - **Dominant Frequency**: Using a Fast Fourier Transform (FFT), find the dominant frequency (in Hz) of the latency spikes in V1. Ignore the DC component (0 Hz). Since the sampling rate is 10 Hz, ensure your frequency bins are scaled correctly.
   - **Hypothesis Test**: Perform a two-sided independent t-test (assuming unequal variances/Welch's t-test) between the latencies of V1 and V2. Extract the p-value.
   - **Distribution Distance**: Calculate the 1D Wasserstein distance (Earth Mover's Distance) between the latency distributions of V1 and V2.
3. **Report Generation**: The Python script should output a JSON file located at `/home/user/report.json` with the exact following structure:
   ```json
   {
     "dominant_freq_v1_hz": 1.25,
     "t_test_p_value": 0.0452,
     "wasserstein_distance": 5.1234
   }
   ```
   *(Note: The values above are placeholders. Round `dominant_freq_v1_hz` to 2 decimal places, and the other two metrics to 4 decimal places).*

Ensure that your bash script `/home/user/analyze.sh` is executable and orchestrates this entire process when run without arguments. Do not install any additional libraries; you may use standard pre-installed tools and Python's `numpy` and `scipy` libraries.