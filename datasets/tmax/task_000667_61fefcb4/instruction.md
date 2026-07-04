You are a support engineer investigating intermittent crashes in a newly deployed log ingestion pipeline. The system occasionally fails with a panic error when processing certain payloads, but the developers cannot reproduce it. 

The pipeline consists of an API gateway (`service_a`), a processing queue (`service_b`), and a data processor (`process.sh` which delegates to a parser).

Your task is to perform a forensic analysis of the logs, reconstruct the timeline of crashes, identify the statistical anomaly in the payloads causing the crashes, and write a regression test.

Here is the system layout:
- `/home/user/ingestion_system/logs/service_a.log` (API Gateway logs, maps request IDs to timestamps)
- `/home/user/ingestion_system/logs/processor.log` (Processor logs, shows crashes but lacks full payload details)
- `/home/user/ingestion_system/raw_data/` (Directory containing raw JSONL dumps of all ingested payloads)
- `/home/user/ingestion_system/process.sh` (The entrypoint script that takes a JSON string as an argument)

**Step 1: Timeline Reconstruction & Anomaly Investigation**
Correlate the crash errors (look for "Panic: unwrap()" in the processor logs) with the API gateway logs to determine the exact `req_id`s that caused the crash. Then, find those payloads in the `raw_data/` directory. 
Identify the common anomalous traits in these payloads.

Extract this information into a CSV file at `/home/user/crash_timeline.csv` with the following exact header and format:
`timestamp,req_id,client_version,duration`
*(Sort the CSV chronologically by timestamp).*

**Step 2: Regression Test Construction**
Based on the anomaly you discovered, write a Bash script at `/home/user/regression_test.sh`.
This script must:
1. Construct a minimal JSON payload that will deterministically trigger the "unwrap()" panic in `/home/user/ingestion_system/process.sh`. The payload must contain a synthetic `req_id` of `"req-test-999"`, the anomalous `client_version`, and the anomalous `duration` value you identified.
2. Execute `/home/user/ingestion_system/process.sh` with this JSON string as its only argument.
3. Check the exit code. If the process crashes (exit code != 0), the regression test should print "Test Passed: Crash Reproduced" and exit with code 0. If it succeeds (exit code == 0), it should print "Test Failed: No Crash" and exit with code 1.

Ensure `/home/user/regression_test.sh` is executable.