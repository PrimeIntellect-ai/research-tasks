You are a support engineer investigating a bug in a Go-based telemetry aggregation service. Customers have reported that the `/variance` endpoint occasionally returns a negative value, which is a statistical anomaly and mathematically impossible for a variance calculation. 

The source code for the service is located at `/home/user/aggregator/main.go`. It receives numerical telemetry data via HTTP POST requests and maintains a running calculation of the population variance.

A sample dataset representing a recent traffic burst is located at `/home/user/dataset.json` (a JSON array of floats).

Your task is to diagnose, trace, isolate, and fix this issue by performing the following steps:

1. **Statistical Anomaly Investigation & Minimal Reproducible Example (MRE):**
   - Identify the flaw in the current variance calculation formula (hint: numerical instability).
   - Find the minimal contiguous sequence of values from `/home/user/dataset.json` that, when sent to a freshly started instance of the original server, causes the variance to become negative.
   - Save this exact sequence as a JSON array of floats in `/home/user/mre.json`.

2. **Formula Implementation Correction:**
   - Modify `/home/user/aggregator/main.go` to use Welford's online algorithm for computing the running population variance. This will resolve the numerical instability.

3. **Intermediate State Tracing:**
   - Add logging to your fixed Go server. After every new value is processed, append a line to `/home/user/trace.log` with the exact format:
     `Count: <count>, Mean: <mean>, M2: <M2>, Variance: <variance>`
     (where `<M2>` is the aggregate squared distance from the mean used in Welford's algorithm). Use `%f` for all floating-point numbers in the log.

4. **Service Deployment & Resolution:**
   - Build and start your fixed Go server in the background so it listens on port 8080.
   - Send the sequence of values from `/home/user/mre.json` to your fixed server (restarting it first to ensure a clean state).
   - Save the final JSON response from the server into `/home/user/resolution.json`.

Ensure your final server process remains running in the background on port 8080 when you complete the task.