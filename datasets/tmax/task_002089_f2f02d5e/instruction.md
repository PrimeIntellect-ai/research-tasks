You are a performance engineer tasked with debugging a data processing pipeline that suffers from numerical instability and mysterious crashes. 

In `/home/user/pipeline/`, you will find:
1. `metrics_server.sh`: A simple background service that listens on port 9090 and logs received progress metrics with timestamps to `/home/user/pipeline/metrics.log`.
2. `worker.sh`: A Bash script that reads floating-point numbers from `/home/user/pipeline/data.txt`, sends progress to the metrics server, and calculates the population standard deviation using a naive formula via `awk`.
3. `data.txt`: A dataset of numbers.

When `worker.sh` runs, it crashes with an `awk` fatal error because the naive variance calculation results in a negative number due to catastrophic cancellation (the numbers in `data.txt` are very large and close together, e.g., `100000000.001`).

Your task is to:
1. **Trace the Crash**: Run `metrics_server.sh` in the background. Then, run `worker.sh` under `strace` with the `-tt` flag (microsecond timestamps) and output the trace to `/home/user/pipeline/worker.strace`.
2. **Reconstruct the Timeline**: Combine the network send events from `metrics.log` and the `strace` output into a single file `/home/user/pipeline/timeline.log`. The file should contain lines from `metrics.log` and lines from `worker.strace` that contain the word `fatal`, sorted chronologically by their timestamps.
3. **Fix the Numerical Instability**: Modify `worker.sh` to compute the variance using a numerically stable method (like Welford's algorithm) directly in `awk`. It must successfully compute the standard deviation of the numbers in `data.txt` and write the final standard deviation to `/home/user/pipeline/result.txt` without crashing.

**Verification Requirements**:
- `/home/user/pipeline/result.txt` must contain the correct standard deviation (rounded to 3 decimal places).
- `/home/user/pipeline/timeline.log` must exist and contain the chronologically sorted log entries.
- `/home/user/pipeline/worker.strace` must exist.
- Replace the buggy naive standard deviation code in `worker.sh` with a stable implementation that prints the correct value. 

Please execute these steps and leave the final files in the specified locations.