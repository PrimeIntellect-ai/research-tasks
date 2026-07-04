You are acting as a capacity planner tasked with building a lightweight resource monitoring tool. You need to gather system metrics, perform network diagnostics to a central metrics server, and schedule this process to run automatically. 

Your objective is to build a Rust-based monitoring tool, set up its environment, and configure it to run as a scheduled task.

Perform the following steps:

1. **Environment Setup**: 
   Add two environment variables to the end of `/home/user/.bashrc`:
   - `METRICS_HOST` set to `127.0.0.1:9999`
   - `LOAD_THRESHOLD` set to `4.0`
   Make sure to export them so that child processes can read them.

2. **Rust Application**:
   Create a new Rust binary project at `/home/user/capacity_monitor`.
   Write a Rust program in `src/main.rs` that does the following:
   - Reads the `METRICS_HOST` and `LOAD_THRESHOLD` environment variables. (If they are not set, the program can exit or panic).
   - Reads the 1-minute load average from `/proc/loadavg`.
   - Reads the `MemAvailable` value (in kilobytes) from `/proc/meminfo`.
   - Performs a connectivity diagnostic by attempting to establish a TCP connection (`std::net::TcpStream::connect`) to the address specified in `METRICS_HOST` with a timeout of 2 seconds.
   - Determines if the 1-minute load average strictly exceeds the `LOAD_THRESHOLD`.
   - Appends a single, valid JSON object on a new line to `/home/user/capacity_log.jsonl`. The JSON object must have exactly these keys:
     - `"timestamp"`: The current Unix timestamp in seconds (integer).
     - `"load_1m"`: The 1-minute load average (float).
     - `"mem_avail_kb"`: The available memory in KB (integer).
     - `"endpoint_reachable"`: Boolean indicating if the TCP connection was successful.
     - `"threshold_exceeded"`: Boolean indicating if `load_1m` > `LOAD_THRESHOLD`.

   Build the project in release mode (`cargo build --release`).

3. **Scheduling**:
   Create a crontab file at `/home/user/planner.cron` that schedules the compiled Rust binary (`/home/user/capacity_monitor/target/release/capacity_monitor`) to run every 5 minutes. 
   Load this file into the user's crontab using the `crontab` command.

Note: You do not need to start a server at `127.0.0.1:9999`; the tool should simply record `false` for `endpoint_reachable` if the connection fails. Ensure the Rust program correctly runs and writes a line to `/home/user/capacity_log.jsonl` when executed manually.