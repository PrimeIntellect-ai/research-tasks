You are acting as an edge computing engineer deploying a telemetry aggregation pipeline on a Linux-based IoT device. The device collects raw sensor data, processes it locally to detect anomalies, and queues email alerts to the administrator if thresholds are exceeded.

Your task is to build and configure this pipeline using C++ and Bash. You do not have root access.

Follow these steps exactly:

1. **System Configuration Management**
   Create a configuration directory `/home/user/edge_config`.
   Inside it, create a file named `sensor.conf` with exactly the following key-value pairs (one per line):
   ```
   THRESHOLD=85.5
   SENSOR_ID=NODE_42
   ALERT_EMAIL=admin@edge.local
   ```

2. **Email Server Configuration**
   The edge device uses `msmtp` to route emails (simulated in this environment). Create an msmtp configuration file at `/home/user/.msmtprc` with the following settings:
   - Account name: `default`
   - Host: `localhost`
   - Port: `2525`
   - From: `edge_node@local`
   - Auth: `off`
   Make sure the file permissions are set to `600`, or the mailer will refuse to run.

3. **C++ Telemetry Analyzer**
   Write a C++ program in `/home/user/src/analyzer.cpp` (you will need to create the `src` directory).
   The program must:
   - Read the threshold value from `/home/user/edge_config/sensor.conf`.
   - Read floating-point numbers from Standard Input (one per line).
   - For every number strictly greater than the threshold, print exactly: `ALERT: SENSOR_ID=[SENSOR_ID_VALUE] VALUE=[NUMBER]` to Standard Output (replace `[SENSOR_ID_VALUE]` with the ID from the config file, and `[NUMBER]` with the floating-point number formatted to 2 decimal places).
   - Compile this program to the executable path `/home/user/bin/analyzer` (create the `bin` directory).

4. **Automation and Text Processing Pipeline**
   Write a bash script at `/home/user/bin/process_telemetry.sh`. Ensure it is executable.
   There is a raw log file provided at `/home/user/data/raw_sensors.log`.
   The bash script must:
   - Use text processing tools (`awk`, `grep`, `sed`, etc.) to extract lines from `/home/user/data/raw_sensors.log` that start with `[DATA]`.
   - Extract the numeric value from those lines (the lines are formatted as `[DATA] <timestamp> | val=<number>`).
   - Pipe these numbers to your compiled `/home/user/bin/analyzer` program.
   - Capture the output of the analyzer. If any alerts are generated, write the captured alerts to a file `/home/user/data/alerts_generated.txt`.

Run your `/home/user/bin/process_telemetry.sh` script to process the data and generate the alerts file.