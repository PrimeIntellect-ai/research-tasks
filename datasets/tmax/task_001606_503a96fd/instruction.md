I need you to act as a data analyst and systems programmer to analyze a suspicious audio recording. We have a baseline dataset of acoustic features from normal operating machinery, and we need to determine if a newly recorded audio sample represents a significant anomaly.

You are provided with:
1. `/app/baseline_metrics.csv`: A dataset containing 1,000 rows. Each row has two comma-separated values: `energy` (float) and `zcr` (zero-crossing rate, float).
2. `/app/anomaly_candidate.wav`: A 16-bit PCM Mono WAV file (44100 Hz) containing the audio to analyze.

Your task is to write a pipeline in **C** that does the following:

1. **Audio Feature Extraction**:
   Parse the `/app/anomaly_candidate.wav` file. Ignore the 44-byte WAV header and read the 16-bit signed integer samples. 
   Calculate two features for the entire audio file:
   - `mean_energy`: The average of the squared sample values (treat samples as floats, calculate sample^2, sum them, divide by number of samples).
   - `zcr`: The zero-crossing rate, defined as the fraction of adjacent sample pairs that have different signs (one positive/zero and one strictly negative, or vice versa).

2. **Statistical Analysis**:
   Parse `/app/baseline_metrics.csv`.
   Using **bootstrap resampling** (with exactly 10,000 iterations), estimate the 95% confidence intervals (using the 2.5th and 97.5th percentiles) for the mean `energy` and mean `zcr` of the baseline dataset. Use a fixed random seed of `42` for reproducibility (using standard `srand(42)` and `rand()`).
   
3. **Hypothesis Testing**:
   Determine if the candidate audio's `mean_energy` or `zcr` falls outside the respective 95% confidence intervals calculated from the bootstrap procedure. If either falls outside, the sample is considered an anomaly.

4. **Service Integration**:
   Write a simple TCP server in C (or wrap your C executable in a bash script using `nc` or `socat`) that listens on `127.0.0.1:8585`.
   When a client connects and sends the exact string `GET_REPORT\n`, the service must reply with a strictly formatted JSON payload (followed by a newline) and then close the connection.

The JSON payload must exactly match this format:
```json
{
  "candidate_energy": 12345.67,
  "candidate_zcr": 0.1234,
  "baseline_energy_ci": [10000.00, 11000.00],
  "baseline_zcr_ci": [0.1000, 0.1500],
  "is_anomaly": true
}
```
*Note: Format all floats to 2 decimal places except for ZCR values, which should be formatted to 4 decimal places.*

Ensure your service remains running so that automated tests can connect to `127.0.0.1:8585`, send `GET_REPORT\n`, and verify your calculations. You can use standard C libraries (`stdio.h`, `stdlib.h`, `math.h`, `sys/socket.h`, etc.).