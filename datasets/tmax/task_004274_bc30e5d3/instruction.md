You are assisting a capacity planner in setting up a local resource monitoring tool. The system is designed to periodically calculate the disk usage of specific project directories and expose this data via a lightweight Rust HTTP server. However, the current setup is broken due to environment variable issues, incorrect filesystem links, and incomplete Rust code.

Your objective is to fix the pipeline, compile the server, and ensure it exposes the correct metrics.

Here are the requirements to get the system fully operational:

1. **Directory Structure and Symlinks:**
   - Raw project data is located in `/home/user/raw_data/proj_alpha` and `/home/user/raw_data/proj_beta` (you will need to create these directories and put a dummy file in each: a 1MB file named `data.bin` in `proj_alpha` and a 2MB file named `data.bin` in `proj_beta` using `dd` or `fallocate`).
   - Create a directory `/home/user/symlinks`.
   - Inside `/home/user/symlinks`, create symbolic links named `alpha` and `beta` that point to the absolute paths of `proj_alpha` and `proj_beta`, respectively.

2. **Metrics Gathering Script:**
   - Create a bash script at `/home/user/gather_stats.sh` that calculates the disk usage (in bytes) of the targets of the symlinks inside `$STORAGE_ROOT/symlinks/`.
   - It must output a JSON file to `/home/user/metrics/usage.json` (create the `/home/user/metrics` directory) in this exact format:
     `{"alpha": <bytes_size>, "beta": <bytes_size>}`
   - Create a runner script at `/home/user/runner.sh` that safely exports the environment variable `STORAGE_ROOT=/home/user` and then executes `/home/user/gather_stats.sh`. Run this runner script once to generate the initial `usage.json`.

3. **Rust Monitoring Server:**
   - Initialize a new Rust project at `/home/user/capacity_server`.
   - Write a simple HTTP server in Rust (you may use `hyper`, `actix-web`, `axum`, or standard library `std::net::TcpListener` without external crates for simplicity).
   - The server must bind to `127.0.0.1:9090`.
   - It must implement two endpoints:
     - `GET /health`: Returns an HTTP 200 OK with the plain text response `{"status": "ok"}`.
     - `GET /metrics`: Reads the file at `/home/user/metrics/usage.json` and returns its contents as application/json. If the file is missing, return an HTTP 404 or 500.
   - Compile the Rust project in release mode and start the server process in the background.

To successfully complete the task, ensure the Rust server is running on port 9090 and serving the correctly calculated metrics from the generated JSON file.