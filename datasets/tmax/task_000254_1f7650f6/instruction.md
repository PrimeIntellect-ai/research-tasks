You are a security researcher analyzing a suspicious metrics daemon. Recently, an anomaly was observed in production: the reported statistical averages occasionally spike to unnatural levels, despite input data being well within expected bounds. We suspect a backdoor or logic bomb has been inserted into the daemon to corrupt query results.

The source code for the daemon is vendored at `/app/analytics-daemon-1.2.3`. 

Your objectives are:
1. Comprehend the existing Go codebase and investigate the anomaly by observing how different queries and HTTP requests affect the statistics.
2. Identify the deliberate perturbation (a hidden backdoor causing statistical anomalies under specific conditions) within the HTTP handlers or statistics logic.
3. Use assertion-based intermediate validation (e.g., sending test requests and querying the results) to confirm your understanding of the anomaly.
4. Fix the Go code to completely remove the backdoor. All submitted values must be recorded exactly as provided, and no hidden headers or parameters should alter the value recorded or the calculation of the statistics.
5. Compile the fixed Go application.
6. Start the server so that it listens on `127.0.0.1:8080`. Leave the process running in the background.

The daemon must expose:
- `POST /submit?value=<float>` to record a metric.
- `GET /stats` to return a JSON response with the calculated `average` and `count`.

Do not change the fundamental structure of the API or the response formats. Focus only on eliminating the statistical anomaly.