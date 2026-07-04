You are tasked with debugging a statistical log analysis service. Our team maintains a vendored Python package at `/app/vendored/log_timeline_api` which provides an HTTP API for reconstructing log timelines across multiple services and identifying statistical anomalies (e.g., unusual latency spikes). 

Recently, a regression was introduced into the `main` branch. A customer reported that the service no longer correctly identifies anomalies when log timestamps cross a day boundary, causing the statistical anomaly detector to drop important events.

The repository at `/app/vendored/log_timeline_api` has about 200 commits. We know that the `v1.0` tag was working perfectly, but the current `HEAD` of the `main` branch is broken.

Your tasks are:
1. **Regression Test Construction:** Write a Python regression test script (e.g., `/home/user/test_regression.py`) that feeds a known sequence of log entries (where at least one event crosses midnight and exhibits a latency spike) into the service's internal analyzer or its API, and uses assertion-based validation to ensure the anomaly is detected.
2. **Bisect the Regression:** Use `git bisect` using your test script to find the exact commit that introduced the bug between the `v1.0` tag and `HEAD`.
3. **Fix the Bug:** Once you find the bad commit, investigate the root cause (it's related to how timestamps and statistical variances are calculated when reconstructing timelines). Fix the code so the regression test passes. Do not just revert the commit if it contains other necessary features; fix the specific mathematical/parsing anomaly.
4. **Deploy the Service:** Start the fixed service so it listens for HTTP traffic on `127.0.0.1:9000`. 
    * The service's entry point is `python -m log_timeline_api.server --port 9000`.
    * You must leave this service running in the background.

The API exposes the following endpoints which must be functional:
- `POST /ingest`: Accepts a JSON array of log objects `[{"service": "web", "timestamp": "2023-10-01T23:59:59Z", "latency_ms": 120}, ...]`.
- `GET /anomalies`: Returns a JSON array of anomalous log objects (those with `latency_ms` > 2 standard deviations above the mean of the ingested logs).

Ensure the server is running on port 9000 before you finish. Do not exit the server process.