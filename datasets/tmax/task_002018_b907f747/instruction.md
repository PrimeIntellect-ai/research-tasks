You are an observability engineer tuning the metric collection pipelines for our internal dashboards. We need a lightweight, custom TCP latency monitor written in Rust that runs periodically and logs metrics in a specific format, along with a log rotation policy to prevent disk exhaustion.

Your task is to implement the following system entirely within `/home/user`:

1. **Rust Latency Monitor**
   - Create a new Rust project named `latency_monitor` in `/home/user/latency_monitor`.
   - Write a Rust program that measures the TCP connection time to two endpoints: `8.8.8.8:53` and `1.1.1.1:53`.
   - Set a connection timeout of 2 seconds.
   - For each endpoint, it must append a single JSON line to `/home/user/latency.log`.
   - The JSON format must be exactly: `{"endpoint": "<ip:port>", "latency_ms": <integer>, "success": <true|false>}`
   - The program should silently exit 0 after attempting both connections and appending the logs.
   - Compile this project in release mode.

2. **Scheduling**
   - Configure the user's crontab to run the compiled release binary (`/home/user/latency_monitor/target/release/latency_monitor`) exactly once every minute.

3. **Log Rotation**
   - Create a logrotate configuration file at `/home/user/logrotate.conf`.
   - It must specifically target `/home/user/latency.log`.
   - Configure it to rotate when the file size exceeds `10k`.
   - It must keep exactly `5` rotated copies.
   - It must `compress` the rotated logs.
   - It must use `missingok` and `notifempty`.

Do not run the cron daemon or logrotate manually—just write the code, build the binary, install the crontab, and create the configuration file. Ensure all paths and JSON keys exactly match these instructions.