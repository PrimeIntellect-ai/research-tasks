You are a performance engineer tasked with debugging an intermittent performance issue in our mathematical processing pipeline. 

We have a pipeline consisting of three simulated microservices: Ingest, Compute, and Writer. Recently, certain requests have been timing out because the Compute service takes unusually long (over 5000ms) to process them. 

Your tasks:
1. **Log Timeline Reconstruction:** The logs for the three services are scattered in `/home/user/logs/ingest.log`, `/home/user/logs/compute.log`, and `/home/user/logs/writer.log`. Reconstruct the timeline to identify the single `RequestID` that experienced an intermittent severe slowdown (took > 5000ms in the compute step).
2. **Statistical Anomaly Investigation:** Look at the `ingest.log` for that specific slow `RequestID`. Identify which statistical feature of the input data caused the issue. The ingest log prints features like Mean, Median, Variance, and StdDev.
3. **Report:** Create a JSON file at `/home/user/anomaly_report.json` with the exact keys `"slow_request_id"` (string) and `"anomaly_feature"` (string, the name of the feature that was exactly 0.0 for this request).
4. **Fix the Bug:** The source code for the compute service is located at `/home/user/math_compute.py`. Analyze the code. You will see that a specific statistical anomaly causes it to fall back to a highly unoptimized function (`slow_fallback_compute`). Modify `/home/user/math_compute.py` so that when this exact statistical anomaly occurs (the identified feature is 0.0), the `normalize_and_compute` function immediately returns a list of zeros of the same length as the input `data`, instead of calling `slow_fallback_compute`.
5. **Verification:** Run the verification script using `python3 /home/user/verify.py`. If your fix is correct, this script will complete in a few milliseconds and automatically create the file `/home/user/success.log`. 

Do not change the signature of `normalize_and_compute`. Ensure the output format of `/home/user/anomaly_report.json` exactly matches the requested keys.