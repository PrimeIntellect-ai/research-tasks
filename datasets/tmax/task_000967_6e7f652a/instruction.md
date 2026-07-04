You are an operations engineer triaging an ongoing incident. Our real-time anomaly detection microservice, written in Rust, is crashing and failing to process incoming query metrics. This service calculates the running variance of query response times using Welford's online algorithm to detect anomalies.

The service is located at `/home/user/anomaly_detector`.
The incoming data feed is located at `/home/user/data/metrics.log`.

Currently, running `cargo run --release -- /home/user/data/metrics.log` crashes with a panic. There are two underlying issues:
1. **Format parsing edge-case:** The parser crashes when encountering malformed scientific notation in the metric values (e.g., missing digits after the 'e' exponent). According to our data ingestion spec, rows with malformed float values should simply be ignored (skipped), not cause a system panic.
2. **Mathematical bug:** Even if you bypass the panic, the variance calculation occasionally yields `NaN` for new query keys, which breaks the downstream query analytics.

Your task:
1. Debug the Rust service in `/home/user/anomaly_detector`.
2. Fix the parsing logic to safely ignore malformed values instead of panicking.
3. Fix the mathematical logic in the Welford variance calculation to prevent `NaN` values (ensure variance is reported as `0.0` when there is only 1 data point).
4. Run the fixed service to process `/home/user/data/metrics.log`.
5. The program should output its final anomalous query summary to `/home/user/corrected_queries.csv`. Ensure your fixes allow the service to successfully write this file without panicking or outputting `NaN`.

**Output format expected in `/home/user/corrected_queries.csv`:**
The service is already programmed to write a CSV with the format `query_id,count,mean,variance`. You do not need to change the CSV formatting code, just fix the bugs preventing it from running successfully.