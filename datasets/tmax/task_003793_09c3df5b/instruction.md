You are a mobile build engineer maintaining our CI/CD pipelines. We have a set of memory profiling logs from different build versions of our mobile app. We need to identify the highest semantic version of the app that does not exceed a strict peak memory limit during its build process.

In the `/home/user/build_logs` directory, there are several log files named `v<version_string>.log` (e.g., `v1.2.3.log`). 
Each file contains a sequence of memory operations, one per line, in the following format:
- `ALLOC <bytes>`: Allocates memory.
- `FREE <bytes>`: Frees memory.

Your task is to write a Python script that:
1. Concurrently processes all log files in `/home/user/build_logs` using a worker pool and a queue (implementing a pattern similar to Go's goroutines and channels, using Python's `threading` or `multiprocessing` with queues).
2. Calculates the peak memory usage (the maximum concurrent bytes allocated at any point in time) for each version. Note that memory starts at 0 for each log.
3. Filters out any versions where the peak memory usage exceeds 500,000 bytes.
4. Uses proper semantic version comparison to determine the absolute highest valid version among the remaining builds. (e.g., `1.10.0` is higher than `1.9.5`).
5. Writes the highest valid version string (exactly as it appears in the filename, without the `.log` extension or the leading `v`) to `/home/user/best_version.txt`.

Constraints:
- You must use a concurrent queue-based pattern in your Python script to process the logs.
- The output file `/home/user/best_version.txt` should contain only the version string (e.g., `1.10.0`).