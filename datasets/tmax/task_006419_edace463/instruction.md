You are the on-call engineer, and you've just received a 3 AM page. The Predictive Autoscaler service has completely crashed, causing critical build pipelines to fail.

Your initial investigation reveals a chain reaction of failures:
1. The metric gatherer, predictor, and scaler services are distributed, logging to different files in `/home/user/logs/`.
2. The predictor service has started throwing exceptions due to a recent numerical instability issue.
3. The nightly model build pipeline is failing, preventing emergency hotfixes from being deployed.

Your tasks are:

**1. Log Timeline Reconstruction**
Analyze the logs in `/home/user/logs/` (`gatherer.log`, `predictor.log`, and `scaler.log`). Find the exact ISO-8601 timestamp of the *very first* event where the scaler service logged an error indicating it received an invalid value (e.g., `NaN` or a math error) from the predictor.

**2. Numerical Instability Diagnosis & Fix**
Inspect `/home/user/service/predictor.py`. The `compute_volatility(data)` function calculates standard deviation but uses a naive, numerically unstable formula ($E[X^2] - (E[X])^2$). When processing large baseline metrics with tiny variations, floating-point precision issues cause this formula to evaluate to a negative number before the square root, causing a `ValueError: math domain error`.
Rewrite `compute_volatility(data)` to be numerically stable (e.g., using Python's built-in `statistics` library or a stable algorithm) so it no longer crashes on large floats.

**3. Build Failure Diagnosis**
The automated build script at `/home/user/service/build.py` runs a suite of tests before packaging. It is currently failing. Diagnose and fix the build script (there may be an unresolved issue introduced by a sloppy late-night git merge).

**4. Incident Report**
Once you have fixed the code, run `python3 /home/user/service/build.py` to ensure it exits with code 0.
Then, create a file at `/home/user/incident_report.txt` containing exactly three lines in the following format:

```text
TIMESTAMP: <Exact ISO Timestamp from Step 1>
FIXED_VOLATILITY: <The result of compute_volatility([1e10, 1e10, 1e10]) using your fixed code, formatted to 2 decimal places (e.g., 0.00)>
BUILD_STATUS: SUCCESS
```