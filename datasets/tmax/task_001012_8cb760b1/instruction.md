**Ticket #9942 - IT Support Queue**

**Subject:** Log pipeline halting due to core dumps in `log_aggregator`

**Description:**
We have an internal CLI tool located at `/app/bin/log_aggregator` that processes incoming CSV log files. Unfortunately, the original source code was lost during a repository migration, and we only have the compiled, stripped binary. 

Recently, the log pipeline has been halting because `log_aggregator` panics and dumps core when it encounters certain corrupted or edge-case log entries. We need you to figure out what specific input is causing the Rust binary to panic.

You have been provided with a small directory of sample log files in `/app/sample_logs/`. Some of these logs process perfectly, while others cause the binary to crash with a panic.

**Your Task:**
1. Investigate the `/app/bin/log_aggregator` binary and the provided `/app/sample_logs/` to determine the exact data condition that triggers the crash.
2. Write a Bash script at `/home/user/sanitizer.sh` that acts as a gatekeeper.

**Specifications for `/home/user/sanitizer.sh`:**
* The script must take exactly one argument: the path to a log file to check.
* If the file is **safe** (i.e., it will NOT crash the binary), the script must print the exact, unmodified contents of the file to standard output and exit with code `0`.
* If the file is **corrupted/evil** (i.e., it contains the data pattern that crashes the binary), the script must output nothing and exit with code `1`.

*Note: Your script must be written in Bash. We will test it against a massive hidden dataset of clean and corrupted logs to ensure it perfectly sanitizes the pipeline.*