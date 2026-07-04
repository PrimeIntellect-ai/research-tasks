You are an operations engineer responding to a Sev-2 incident regarding our telemetry pipeline. The pipeline processes high-throughput floating-point sensor data, but downstream consumers are reporting two major issues:
1. Significant data loss during the ingestion phase.
2. Unacceptable numerical drift in the calculated moving averages.

The system is deployed under `/app/` and consists of three components:
1. `redis` (running on standard port 6379, already started)
2. `ingest-svc`: A Go service in `/app/ingest` (listens on port 8081). It receives base64-encoded JSON payloads and forwards them to the aggregator.
3. `aggregator-svc`: A Go service in `/app/aggregator` (listens on port 8082). It maintains a running sum and count in memory (backed up to Redis) to compute the average of the sensor readings.

Your tasks:
1. **Dependency & Encoding Troubleshooting**: `ingest-svc` is failing to parse about 30% of the incoming base64 JSON packets. Investigate `/app/ingest`. There is a known dependency conflict in its `go.mod` causing the custom JSON parser to silently truncate payloads. Downgrade or replace the faulty library to ensure 100% of payloads are successfully decoded and forwarded.
2. **Floating-point Precision Repair**: Inspect `/app/aggregator/main.go`. The service calculates the running average using a naive sum. Due to the high volume of data and the mix of very large and very small floating-point numbers, catastrophic cancellation is causing severe precision loss. Modify the Go code to use a numerically stable algorithm (such as Kahan summation or Welford's algorithm) or fix any erroneous type conversions. 
3. **Re-integration**: Ensure both services compile successfully. Use the provided script `/app/start.sh` to launch both services in the background.

Once both services are running and fixed, run the test harness:
`bash /app/test_harness.sh`
This script will pump 50,000 sensor readings into `ingest-svc` and output the final computed average to `/home/user/final_average.txt`.

Success is determined strictly by the accuracy of the final average. The automated verifier will calculate the Absolute Error between your system's output in `/home/user/final_average.txt` and the true mathematical average. Your Absolute Error must be strictly less than `0.0001`.