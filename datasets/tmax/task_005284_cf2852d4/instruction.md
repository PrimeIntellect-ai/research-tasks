You are a security researcher analyzing a suspicious containerized application. During your investigation, you extracted a compiled binary used by the malware, located at `/app/malware_oracle`. This binary reads container log files, parses the query execution times from the logs, and computes a specific "anomaly risk score" based on the variance of those times.

To understand the malware better, your team reverse-engineered the binary and created a Python clone, which is provided as a vendored package at `/app/malware_score_clone-1.2.0`. 

However, the current Python implementation is flawed:
1. **Query Result Debugging:** It fails to correctly parse the full query execution times from certain container log formats due to a bug in its text processing logic.
2. **Numerical Instability:** When processing logs where query execution times are extremely large but very close in value (a common scenario in these specific container logs), the script suffers from catastrophic cancellation, resulting in an incorrect variance calculation and a wildly inaccurate final score.

Your objective is to fix the Python codebase in `/app/malware_score_clone-1.2.0/scorer.py` so that its output is **bit-exact equivalent** to the `/app/malware_oracle` binary for any given log file. 

The entry point for your script is:
`python3 /app/malware_score_clone-1.2.0/scorer.py <path_to_log_file>`

Both the oracle binary and your fixed script must output the exact same string (a single float value formatted to 6 decimal places, followed by a newline). Fix the bugs in the Python script to perfectly match the oracle's behavior.