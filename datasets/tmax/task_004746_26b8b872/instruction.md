You are tasked with debugging and fixing a critical regression in a log timeline analysis tool, and restoring a multi-service logging pipeline.

You have been provided with a local Git repository at `/home/user/timeline_analyzer` containing a C application. This tool (`analyzer.c`) is designed to parse custom binary log formats, skip corrupted or malformed entries, and reconstruct a chronologically sorted log timeline. 

Recently, a regression was introduced somewhere in the last 200 commits. On certain corrupted log inputs, the analyzer now either segfaults or drops subsequent valid logs instead of recovering cleanly.

Additionally, the tool runs as part of a multi-service architecture. In `/home/user/env`, there is a `startup.sh` script that launches a Redis instance and a Python-based log ingestor service. The ingestor receives raw logs and pushes them into a Redis list called `raw_logs`.

Your objectives are:
1. **Bisect the Regression:** Identify the exact commit hash that introduced the bug. Write this full 40-character commit hash to `/home/user/bad_commit.txt`.
2. **Fix the Bug:** Create a minimal reproducible example, fix the bug in `analyzer.c` on the `main` branch, and ensure it correctly skips corrupted entries (where the declared payload length exceeds the remaining buffer) without crashing or skipping valid subsequent logs.
3. **Re-integrate the Service:** Modify the configuration or arguments so that the fixed analyzer successfully pulls from the Redis list `raw_logs` at `redis://127.0.0.1:6379`, processes the logs, and writes the reconstructed timeline to `/home/user/final_timeline.log`.

The analyzer can be compiled using the provided `Makefile` by running `make`. It accepts a file via `./analyzer -f <filepath>` or a redis queue via `./analyzer -r <redis_host> -q <queue_name> -o <output_file>`.

Verify your fix thoroughly. The final compiled binary must reside at `/home/user/timeline_analyzer/analyzer`.