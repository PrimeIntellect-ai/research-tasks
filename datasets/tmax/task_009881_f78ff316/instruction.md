You are an edge computing engineer deploying a robust telemetry aggregator to an IoT gateway device. 

Your task is to create a Rust-based daemon that processes rolling sensor logs, combined with a custom Bash supervisor script to manage its lifecycle.

Here are the requirements:

1. Setup the Environment:
   - Create directories: `/home/user/sensor_data`, `/home/user/metrics`, and `/home/user/run`.
   - Initialize a new Rust project at `/home/user/iot_aggregator`.

2. The Rust Aggregator Application:
   - Write a Rust program in `/home/user/iot_aggregator` that continuously monitors the file pointed to by a symlink at `/home/user/sensor_data/latest.log`.
   - The log lines have the format: `[TIMESTAMP] sensor=ID temp=XX.XC humidity=YY% status=STATUS`
   - Example: `[2023-10-25T10:00:00Z] sensor=A1 temp=45.2C humidity=55% status=OK`
   - The application must parse these lines. It must IGNORE lines where `status=ERROR` or `status=OFFLINE`.
   - Every time it reads a valid line, it should update and write a JSON file to `/home/user/metrics/current.json` with the exactly following structure:
     `{"latest_temp": 45.2, "latest_humidity": 55.0, "valid_readings_count": 1}`
     (Increment the count for each valid reading processed during the process's lifetime).
   - **Lifecycle Handling:** The Rust application must catch the `SIGTERM` signal. When a `SIGTERM` is received, it must write `{"status": "shutting_down"}` to `/home/user/metrics/state.json` and then cleanly exit with code 0.

3. The Supervisor Script:
   - Create a bash script at `/home/user/supervisor.sh` (make it executable).
   - When run, it should start the compiled Rust application in the background.
   - It must write the PID of the Rust application to `/home/user/run/aggregator.pid`.
   - It must monitor the process. If the process exits unexpectedly (not via a controlled shutdown where we kill it), the supervisor should restart it and update the PID file.

4. Final Output:
   Build your Rust application (`cargo build --release`). 
   Create a file `/home/user/deployment_report.txt` with the following format:
   ```
   BINARY_PATH=/home/user/iot_aggregator/target/release/iot_aggregator
   SUPERVISOR_PATH=/home/user/supervisor.sh
   PID_FILE=/home/user/run/aggregator.pid
   ```

Note: You can use external crates like `serde`, `serde_json`, and `ctrlc` by adding them to your `Cargo.toml`. 
Do not assume root privileges. Execute all configurations within `/home/user`.