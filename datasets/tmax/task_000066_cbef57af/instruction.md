You are a security researcher investigating a series of crashes in a backend data pipeline. The pipeline processes CSV logs of network events using a vendored version of `xsv` (a fast CSV command line toolkit written in Rust). 

Recently, the pipeline started crashing with a Rust `unwrap()` panic when processing certain external feeds. We suspect a malicious actor is injecting crafted edge-case data to trigger this denial-of-service.

Your tasks are:
1. **Fix the Build**: The vendored package source is located at `/app/vendored/xsv-0.13.0`. The `Makefile` was recently modified and is currently broken. Identify the perturbation in the `Makefile`, fix it, and compile the `xsv` binary (ensure the executable is available at `/app/vendored/xsv-0.13.0/target/release/xsv`).
2. **Delta Debugging**: Several raw payload files are located in `/app/raw_feeds/`. Some trigger the core dump, others do not. Use bash scripting, delta debugging, or stack trace analysis to isolate the exact statistical anomaly or string pattern causing the `unwrap()` panic in `xsv stats`.
3. **Build a Sanitizer**: Once you understand the exploit payload, write a Bash script at `/home/user/sanitize_feed.sh`. 
   - The script must read a CSV file path as its first argument (e.g., `./sanitize_feed.sh input.csv`).
   - It must output the sanitized CSV data to `stdout`.
   - It must drop any row containing the malicious payload, leaving the rest of the CSV intact and valid.
   - If the file does not exist or is empty, it should exit with code 1.

An automated evaluation will test your `/home/user/sanitize_feed.sh` script against an unseen corpus of "clean" and "evil" log files. To succeed, your script must preserve 100% of the clean data rows while stripping out 100% of the malicious rows, without altering the CSV header or formatting.