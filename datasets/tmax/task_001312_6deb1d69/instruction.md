You are a DevOps engineer debugging a mathematical log analytics pipeline that has been failing in production. The pipeline is supposed to process network metrics, but it frequently deadlocks under high contention or when receiving malformed packets. Additionally, it has been reporting incorrect mathematical metrics due to precision loss.

Your task has two main phases:

**Phase 1: Multi-Service Pipeline Repair**
Under `/app/pipeline/`, there are three services designed to work together:
1. `pcap-streamer`: Reads packet capture files and streams parsed metrics over TCP.
2. `math-analyzer`: A multithreaded Rust service that computes complex risk metrics from the streamed data.
3. `alert-sink`: Collects results and writes them to disk.

Currently, the services are not connecting to each other. A startup script `/app/pipeline/start.sh` attempts to bring them up, but the end-to-end flow fails. 
- You must reconfigure the environment variables and configuration files in `/app/pipeline/config/` so that `pcap-streamer` connects to `math-analyzer`, and `math-analyzer` forwards valid calculations to `alert-sink`. 
- Ensure that the final output is written successfully to `/app/pipeline/output/alerts.log` when you run `/app/pipeline/start.sh`. Use `strace` or network packet capture tools (like `tcpdump` or `tshark`) if you need to diagnose where the connections are failing.

**Phase 2: Debugging and Adversarial Filtering**
The `math-analyzer` (Rust code located in `/app/math-analyzer/`) has several critical bugs:
1. **Concurrency / Deadlock:** It deadlocks when processing certain sequences of metrics.
2. **Infinite Recursion / Loop Termination:** Certain malformed "evil" metrics cause infinite recursion when calculating dependency graphs.
3. **Precision Loss:** Floating-point precision loss in the risk score calculation causes clean logs to be flagged incorrectly.

You must fix the Rust codebase in `/app/math-analyzer/`. 
Once fixed, compile it. The binary `cargo build --bin filter_cli` will be used to test your solution.
Your compiled CLI must act as a filter. When invoked as `/app/math-analyzer/target/debug/filter_cli <file_path>`, it should read a metric log file and:
- Output exactly `ACCEPT` to `stdout` and exit with code `0` if the log is mathematically valid and safe.
- Output exactly `REJECT` to `stdout` and exit with code `1` if the log contains infinite-loop-inducing anomalies or triggers the deadlock scenario.

You have access to two corpora for testing:
- `/app/corpora/clean/`: Contains 50 clean metric files.
- `/app/corpora/evil/`: Contains 50 malicious/malformed metric files.

Your final CLI must successfully `ACCEPT` 100% of the clean corpus and `REJECT` 100% of the evil corpus.

Do not change the fundamental mathematical formulas in the analyzer, but fix the precision bugs (e.g., changing data types or operation order where mathematically sound) and fix the deadlock/loop bugs.