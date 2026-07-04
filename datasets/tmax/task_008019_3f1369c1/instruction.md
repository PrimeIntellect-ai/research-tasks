You are a Site Reliability Engineer (SRE) investigating a critical issue with your team's custom uptime monitoring service. The service calculates a health metric using an Exponentially Weighted Moving Average (EWMA) based on ping latencies. Recently, the monitoring pipeline started failing: it is throwing tracebacks in production and the health metric is failing to converge, instead returning `NaN` or `Infinity`.

You have been granted access to the repository located at `/home/user/uptime_monitor`. 
The `main` branch is currently broken. A known good state was tagged as `v1.0`.

Your task requires you to complete the following phases:

1. **Regression Finding:** Use git bisection to identify the exact commit hash that introduced the errors.
2. **Environment Misconfiguration Repair:** The failing code also introduced a reliance on an environment variable that is not properly configured, causing a traceback before the metric can even be calculated. Analyze the traceback by running `python run_analysis.py`, identify the missing/misconfigured environment variable, and fix the environment or the code handling it so the script executes without crashing.
3. **Convergence Failure Repair:** Once the script runs, you will see the health metric diverges to infinity. Inspect the EWMA mathematical implementation in `analyzer.py`. Identify the mathematical typo causing the convergence failure and correct it so the metric stabilizes.
4. **Forensics Reporting:** After fixing the code, run `python run_analysis.py` again. It will succeed and print the final health metric.
5. Create a report file at `/home/user/forensics_report.json` with the following exact structure:
```json
{
  "bad_commit": "<full_40_character_git_commit_hash>",
  "fixed_metric": <float_value_rounded_to_2_decimal_places>
}
```

Constraints and details:
- Do not change the random seed or the synthetic data generation logic in the script.
- Ensure the EWMA formula correctly balances the current value and the historical value (they should sum to 1.0 weight).
- The `bad_commit` in your report must be the exact commit that introduced the environment and mathematical bugs.