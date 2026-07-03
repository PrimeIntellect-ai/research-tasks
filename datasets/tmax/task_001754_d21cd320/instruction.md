Wake up, you're on call! It's 3:00 AM and our PagerDuty just fired. The primary metrics aggregation service has crashed in production.

We have gathered the initial forensics:
1. There is a stack trace log from the crash at `/home/user/logs/crash.log`.
2. The source code for the service is located at `/home/user/service/aggregator.py`.
3. There is a production runner script at `/home/user/service/run_production.py` that relies on the `aggregator.py` module.

From a quick glance at the dashboard before it went down, we suspect two distinct issues:
1. **Connection Retries:** Under heavy load or timeouts (simulated in the code), the service seems to leak frames or tasks, eventually resulting in a crash.
2. **Data Corruption / Math Errors:** Just before the crash, the standard deviation metrics reported `NaN` or threw math domain errors, suggesting severe numerical instability in the variance calculation when processing large, closely spaced floating-point values.

Your tasks:
1. Analyze the stack trace in `/home/user/logs/crash.log` to identify the failure point.
2. Fix the infinite recursion bug in `fetch_data_with_retry` within `/home/user/service/aggregator.py`.
3. Fix the numerical instability in the `compute_standard_deviation` method in `/home/user/service/aggregator.py`. You may use Python's built-in `statistics` module or implement Welford's online algorithm to ensure precision.
4. Once you have fixed `aggregator.py`, execute the production runner: `python3 /home/user/service/run_production.py`.

The runner will process the pending batch of metrics and, if successful, automatically write the results to `/home/user/metrics_output.json`. 

Ensure that `/home/user/metrics_output.json` is successfully generated and contains the exact JSON output expected by the downstream systems. Do not modify `run_production.py`.