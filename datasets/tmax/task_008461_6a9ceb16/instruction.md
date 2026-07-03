You are an observability engineer tasked with building a lightweight, custom storage monitoring daemon and its lifecycle management script. Your goal is to track the disk usage of simulated application environments (directories) and expose this data as Prometheus metrics for our dashboards.

Please implement the following components from scratch. You must work within the `/home/user/exporter` directory (create it if it doesn't exist).

**Step 1: The C++ Monitoring Daemon**
Create a C++ program at `/home/user/exporter/main.cpp` that fulfills these requirements:
1. It must be written in C++17.
2. It must accept exactly two command-line arguments:
   - `argv[1]`: The absolute path of the directory to monitor.
   - `argv[2]`: The absolute path of the output metrics file.
3. Once started, it should run an infinite loop. Every 1 second (use `std::this_thread::sleep_for`), it must:
   - Calculate the total size in bytes of all files within the directory specified in `argv[1]` (recursively).
   - Completely overwrite the file specified in `argv[2]` with a single line of text in the Prometheus metric format:
     `mock_container_storage_bytes{path="<directory_path>"} <total_size_in_bytes>`
   - Ensure a newline `\n` is added at the end of the line, and flush/close the file stream so the metric is immediately readable by other processes.

**Step 2: The Lifecycle Management Script**
Create an interactive Bash script at `/home/user/exporter/lifecycle.sh` to manage the compilation and execution of your daemon. It must accept the following subcommands:
1. `./lifecycle.sh build`
   - Compiles `/home/user/exporter/main.cpp` into an executable named `/home/user/exporter/bin` using `g++ -std=c++17 -O2`.
2. `./lifecycle.sh start <monitor_dir> <metrics_file>`
   - Starts `/home/user/exporter/bin` in the background, passing `<monitor_dir>` and `<metrics_file>` as arguments.
   - Saves the background process ID (PID) to `/home/user/exporter/pidfile`.
3. `./lifecycle.sh stop`
   - Reads the PID from `/home/user/exporter/pidfile`.
   - Sends a `SIGTERM` (using `kill`) to that PID.
   - Deletes `/home/user/exporter/pidfile`.

**Step 3: Execution**
There is a pre-existing simulated container directory at `/home/user/mock_container`.
1. Make sure your script is executable (`chmod +x`).
2. Run `./lifecycle.sh build`.
3. Run `./lifecycle.sh start /home/user/mock_container /home/user/metrics.prom`.

Leave the daemon running in the background when you are finished. Automated tests will evaluate your source code, invoke the bash script, verify the metrics output format, and ensure process termination via your `stop` command works correctly.