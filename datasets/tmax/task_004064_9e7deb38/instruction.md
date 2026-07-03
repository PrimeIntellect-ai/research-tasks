You are an on-call engineer who just received a high-severity page at 3:00 AM. The background anomaly detection pipeline, which processes incoming server metrics, has suddenly started failing, leaving downstream dashboards empty.

Your initial investigation reveals the following:
- The cron job logs are located at `/home/user/logs/cron_error.log`. 
- The anomaly detection codebase is a Git repository located at `/home/user/anomaly_detector`.
- The pipeline processes metric batches from `/home/user/data.csv`.

Your objectives:
1. **Analyze the Logs**: Review the traceback in `/home/user/logs/cron_error.log` to understand why the pipeline is crashing. It appears to be a convergence failure caused by a recent code change.
2. **Find the Regression**: Use `git bisect` (or your preferred debugging method) within the `/home/user/anomaly_detector` repository to identify the exact commit that introduced the bug.
3. **Record the Bad Commit**: Write the full, 40-character Git commit hash of the bad commit to a file named `/home/user/bad_commit.txt`.
4. **Fix the Bug**: Repair the floating-point precision or convergence logic in `detector.py` on the `main` branch so that it successfully terminates and computes the metrics accurately.
5. **Generate the Output**: Run the fixed script using `python /home/user/anomaly_detector/detector.py --input /home/user/data.csv --output /home/user/fixed_metrics.csv`. 

Ensure that `/home/user/fixed_metrics.csv` is correctly generated and contains the processed results without throwing any exceptions.