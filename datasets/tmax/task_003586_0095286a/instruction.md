You are an SRE investigating a mysterious recurring crash in a legacy data pipeline. 

The core of the pipeline is a long-running service that ingests telemetry data. The service is provided as a compiled, stripped binary located at `/app/telemetry_ingest`. Recently, it has been crashing unpredictably, taking down the pipeline. When it crashes, system logs indicate that the process abruptly terminates, and right before dying, it spikes in memory usage (a rapid memory leak) before hitting a Rust `unwrap()` panic.

We do not have the source code or build environment for `/app/telemetry_ingest`. 

You have been provided a sample of recently ingested data in JSON Lines (JSONL) format, located in `/home/user/raw_logs/`. Some of the files in this directory contain the malformed edge-case data that triggers the panic, while others process perfectly fine.

Your objective:
1. **Error Diagnosis & Delta Debugging:** Use the provided binary and the sample logs to reproduce the crash. Use test minimization/delta debugging techniques to isolate the exact JSON payload characteristics (specific key-value combinations or missing fields) that cause the stripped Rust binary to panic on `unwrap()`.
2. **Sanitization Filter:** Once you understand the root cause, write a robust Bash-executable filter script at `/home/user/sanitize.sh`. 
   - The script must read a JSON Lines stream from standard input (`stdin`).
   - It must evaluate each JSON object line by line.
   - It must output (to `stdout`) *only* the JSON lines that are safe for `/app/telemetry_ingest` to process.
   - It must silently drop any JSON line that would trigger the panic/memory leak in the binary.
   - Safe lines must be printed exactly as they were received, with no structural mutations.

Ensure your `/home/user/sanitize.sh` script is executable (`chmod +x`). 

An automated test suite will pipe a large, hidden dataset of both perfectly clean telemetry logs and adversarial, crash-inducing logs through your script. Your script will be evaluated on whether it successfully preserves 100% of the clean logs and drops 100% of the crash-inducing logs.