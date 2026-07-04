You are a container specialist tasked with wrapping a problematic legacy microservice. 

We have a legacy log-processing binary located at `/app/legacy_processor`. This is a stripped binary that reads log lines from `stdin`, performs an expensive cryptographic transformation, and writes the processed lines to `stdout`. 
Unfortunately, the binary is unstable: it crashes (segfaults) whenever it encounters a malformed input line containing the string `POISON_PILL`.

Your task is to write a highly performant Process Supervisor and Load Balancer in C (`/home/user/supervisor.c`) that wraps this legacy binary to achieve high throughput and fault tolerance.

Requirements for `/home/user/supervisor.c`:
1. **Environment Configuration**: 
   - Read `WORKER_COUNT` (integer). If unset, default to 4.
   - Read `LOG_PATH` (string). If unset, default to `/home/user/logs/processed.log`.

2. **Process Management & Supervision**:
   - Spawn `WORKER_COUNT` instances of `/app/legacy_processor` as child processes.
   - If any child process exits or crashes for any reason, your supervisor must detect this (e.g., via `waitpid` or `SIGCHLD`) and immediately spawn a replacement worker to maintain exactly `WORKER_COUNT` active workers.

3. **Data Routing (Load Balancing)**:
   - Your supervisor will receive a massive stream of lines via its own `stdin`.
   - It must distribute these lines to the active child processes in a round-robin fashion using pipes. 
   - Ensure you do not write to a broken pipe if a worker has crashed; buffer or re-route the line to the next available worker or the restarted worker.

4. **Log Aggregation & Rotation**:
   - The supervisor must read the `stdout` of all child processes and aggregate the output into the file specified by `LOG_PATH`.
   - **Log Rotation**: Whenever the size of the file at `LOG_PATH` reaches or exceeds exactly 1,048,576 bytes (1 MB) *after* writing a complete line, it must be rotated. Rename it to `<LOG_PATH>.1` (overwriting any existing `.1` file) and create a new `<LOG_PATH>` file for subsequent output.

5. **Performance (The Metric)**:
   - Processing a single line takes the legacy binary roughly 10 milliseconds. Sequential processing is too slow.
   - Your supervisor must utilize the worker pool effectively. An automated test will evaluate the execution time of your compiled supervisor against a test dataset of 2,000 lines (including several poison pills) using 8 workers.
   - To pass, your implementation must complete the processing in under **4.0 seconds**.

Write a build script at `/home/user/build.sh` that compiles your C program to `/home/user/supervisor` using `gcc` with `-O3`. 
Create any necessary directories required for the default paths. Ensure your C code handles standard POSIX system calls gracefully.