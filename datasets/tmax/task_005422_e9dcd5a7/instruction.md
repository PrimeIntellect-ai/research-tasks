You are an Incident Response DevOps Engineer. We have experienced a security incident and need to analyze our access logs to find anomalous behavior.

Here is what you need to do:
1. **Extract Configuration:** You have been provided an image at `/app/config.png` which contains a screenshot of a dashboard. Use OCR (e.g., `tesseract`) to extract the text. It contains two crucial pieces of information: an `AUTH_TOKEN` and a statistical `THRESHOLD` formula for anomaly detection.
2. **Database Recovery:** Our logging database at `/app/logs.db` was corrupted during a hard crash, but its Write-Ahead Log (`/app/logs.db-wal`) is intact. Recover the database so it can be queried. The database contains a table `access_logs` with columns `ip_address` and `request_count`.
3. **Fix the Analyzer:** There is a broken Python script at `/app/analyzer.py`. It is supposed to calculate the mean and sample standard deviation of the `request_count` across all IPs in the recovered database, and flag IPs whose request counts strictly exceed the `THRESHOLD` formula you extracted from the image. Correct the statistical formula implementation in the script.
4. **Regression Test:** Create a minimal reproducible regression test at `/app/test_analyzer.py` that imports your fixed analyzer function, runs it on a mock list of `(ip, count)` tuples, and asserts the correct anomalous IPs are returned.
5. **Serve the Results:** Write and start a Python HTTP server (you may use `http.server` or any installed framework) listening on `127.0.0.1:8000`. 
   - It must expose a `GET /anomalies` endpoint.
   - It must require an `Authorization: Bearer <AUTH_TOKEN>` header, where `<AUTH_TOKEN>` is the token extracted from the image. Return a 401 status code if the token is missing or incorrect.
   - On success, it must query the recovered database using your fixed analyzer and return a JSON response in the format: `{"anomalous_ips": ["ip1", "ip2"]}` (sorted alphabetically).

Leave the server running in the background or foreground so that our automated verification system can query it.