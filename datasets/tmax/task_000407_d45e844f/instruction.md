You are an application performance engineer trying to automate the detection of anomalous performance profiles. 

We recorded a baseline test run of our application's UI. The recording is available as a video at `/app/ui_test_run.mp4`. To simplify analysis, the UI was engineered to output its frame latency visually: the average value of the Red channel across all pixels in a given frame represents the application's latency for that frame in milliseconds.

We also have a collection of performance profile traces from user machines, stored as JSON arrays of latency values in `/app/corpus/`. Some of these traces are from users with heavy background bloatware ("evil"), and some are from clean machines ("clean").

Your task is to build a statistical pipeline to analyze the baseline video and classify the traces.

**Step 1: Baseline Extraction and Analysis**
1. Extract the latency timeseries from `/app/ui_test_run.mp4`. For each frame in order, calculate the average Red channel pixel value (0-255). This is the latency in milliseconds.
2. Calculate the 95% Bootstrap Confidence Interval for the mean latency of this video trace. Use `scipy.stats.bootstrap` with exactly 10,000 resamples, `method='percentile'`, and `random_state=42`. Write the result to `/home/user/ci.txt` in the format `lower_bound,upper_bound` (rounded to 4 decimal places).
3. Fit the extracted baseline latencies to a Normal distribution using Maximum Likelihood Estimation (MLE) or standard sample mean/stddev. Write the parameters to `/home/user/fit.txt` in the format `mean,stddev` (rounded to 4 decimal places).

**Step 2: Trace Classification (Hypothesis Testing)**
Write a Python script at `/home/user/classifier.py` that takes a single file path as a command-line argument. The file will be a JSON array of integers representing frame latencies.
Your script must:
1. Load the video baseline latency array.
2. Load the JSON trace array.
3. Perform a 2-sample Kolmogorov-Smirnov test (`scipy.stats.ks_2samp`) comparing the JSON trace to the video baseline trace.
4. If the p-value is less than 0.05, the trace is statistically different from the baseline (anomalous). The script must **reject** the trace by exiting with status code `1`.
5. If the p-value is greater than or equal to 0.05, the trace matches the baseline. The script must **accept** it by exiting with status code `0`.

Ensure your classifier is robust and efficient.