You are a Machine Learning Engineer preparing training data for an anomaly detection model that monitors a thermal process. You have two data sources from a recent experiment:
1. A video recording of the process: `/app/experiment_run.mp4`
2. Telemetry data from a sensor: `/app/telemetry.csv` (Format: `frame_index,temperature` - with a header, 0-indexed)

Your task is to build a reproducible pipeline that extracts features from the video, joins it with the telemetry data, and engineers statistical features using a custom Go program.

Step 1: Video Feature Extraction & Joining
Extract the average grayscale pixel intensity (brightness) for every frame in `/app/experiment_run.mp4`. You may use `ffmpeg` (e.g., scaling to 1x1 pixel and extracting the raw value) or write a script to compute this. 
Join this extracted sequence with `/app/telemetry.csv` by matching the frame index. The joined data should conceptually be rows of `brightness,temperature`.

Step 2: Statistical Feature Engineering (Go Program)
To ensure our pipeline is performant and verifiable, write a Go program at `/home/user/feature_extractor.go` and compile it to exactly `/home/user/bin/feature_extractor`. 

The Go program must behave exactly as follows:
- Read CSV lines from `standard input` containing two comma-separated floats: `brightness,temperature` (no header).
- Maintain a rolling window of the most recent `10` rows (inclusive of the current row).
- For the first 9 rows, do not output anything.
- From the 10th row onwards, for every row, calculate and print a comma-separated line to `standard output` with the following engineered features:
  1. `mean_brightness`: The arithmetic mean of the brightness over the 10-row window.
  2. `temp_ci_lower`: The 95% confidence interval lower bound for the temperature over the 10-row window. Use the formula: `mean_temp - 1.96 * (s_temp / sqrt(10))`, where `s_temp` is the sample standard deviation (using n-1 = 9 in the denominator).
  3. `temp_ci_upper`: The 95% confidence interval upper bound for the temperature over the 10-row window (using `+ 1.96`).
  4. `anomaly_flag`: An integer (`1` or `0`). `1` if the *current* row's brightness is strictly greater than `mean_brightness + 1.5 * s_brightness` (where `s_brightness` is the sample standard deviation of brightness for the window), otherwise `0`.

Output Format: Print the three float values formatted to exactly 4 decimal places, followed by the integer flag. Example line: `120.4500,45.2134,50.1234,0`.

Step 3: Pipeline Execution
Run your joined data (from Step 1) through your compiled `/home/user/bin/feature_extractor` program and save the final output to `/home/user/training_features.csv`.