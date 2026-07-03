You are a support engineer tasked with collecting diagnostics and fixing a broken telemetry processing pipeline. 

We have a Go application located at `/home/user/telemetry` that reads raw binary sensor data from `/home/user/data/raw_telemetry.bin`, processes it concurrently by shelling out to a legacy closed-source binary, and aggregates the results.

However, the pipeline is currently failing for two reasons:
1. **Corrupted Input Crashes:** The legacy binary at `/app/telemetry_decoder` is a stripped, black-box executable that occasionally crashes (segfaults/panics) when processing certain malformed records in our raw data. When it crashes, the Go pipeline fails to handle the error properly and the entire batch is aborted. You need to investigate the binary to determine what specific input characteristics cause it to crash, and modify the Go code to filter out these "poison pills" before passing them to the decoder.
2. **Data Loss (Race Condition):** Even when running on clean data, the Go pipeline drops records. There is a concurrency bug in `/home/user/telemetry/main.go` where worker goroutines are writing their outputs to a shared data structure improperly.

Your task:
1. Analyze `/app/telemetry_decoder` to understand the input conditions that trigger a crash.
2. Fix the Go codebase in `/home/user/telemetry` to identify and safely discard corrupted inputs *before* they reach the binary.
3. Fix the race condition in the Go codebase so that no valid data is dropped.
4. Ensure the pipeline processes the data highly concurrently.
5. The output must be written to `/home/user/telemetry/output.json` as a JSON map of `{"record_id_integer": "decoder_output_string"}`.

To succeed, you must optimize the Go pipeline so that it completes the processing of `/home/user/data/raw_telemetry.bin` (which contains 10,000 records) quickly. Your final code must be runnable via `cd /home/user/telemetry && go build && ./telemetry`.