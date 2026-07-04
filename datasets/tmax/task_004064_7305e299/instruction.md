You are an automation specialist tasked with building a high-throughput telemetry data processing pipeline. We have an environment where IoT sensor logs are streamed into a message broker, and we need a C-based worker to sanitize, aggregate, and report on this data in real-time. 

Your goal is to fix the existing service infrastructure, write a C program to process the logs, and ensure your data sanitization logic can withstand malicious inputs.

### System Architecture & Service Glue
We have a multi-service architecture running locally. A startup script `/app/start_services.sh` is provided, which spawns:
1. **Redis Server**: Acts as the message broker on port 6379.
2. **Telemetry Emitter**: A Python script that constantly pushes raw CSV logs to a Redis List called `raw_logs`.
3. **Nginx Web Server**: Intended to serve generated HTML reports.

**Task 1: Service Configuration**
The Nginx configuration file provided at `/home/user/nginx.conf` is currently broken. Nginx fails to start because it tries to bind to port 80 (requires root) and points to a non-existent web root. 
- Modify `/home/user/nginx.conf` so Nginx listens on port **8080**.
- Change the document root to `/home/user/reports`.
- Start the services using `/app/start_services.sh`.

**Task 2: Data Processing & Feature Extraction in C**
Write a C program (e.g., `processor.c`) that compiles to `/home/user/log_tool`. You may use standard POSIX libraries and `hiredis` (which is installed on the system).

The C program must have two modes of operation:

**Mode A: Offline Filtering & Sanitization**
Command signature: `./log_tool --filter <input_file.csv> <output_file.csv>`
The CSV format is: `timestamp,sensor_id,temperature,metadata`
You must implement a strict sanitization filter. Some logs contain malicious payloads in the `metadata` field (e.g., SQL injection or XSS attempts). You must discard the entire row if the `metadata` field contains any of the following substrings (case-insensitive):
- `<script>`
- `javascript:`
- `UNION SELECT`
- `onload=`

Your filter will be tested against two offline corpora provided in the environment. Your goal is to preserve 100% of the clean logs and reject 100% of the malicious logs.

**Mode B: Real-Time Aggregation & Template Generation**
Command signature: `./log_tool --daemon`
When running in daemon mode, the program should:
1. Continuously pop logs from the Redis list `raw_logs` (using `BLPOP` or similar).
2. Apply the sanitization filter described above.
3. Perform **time-based bucketing**: Group the valid logs into 1-minute windows based on the Unix `timestamp` field.
4. Perform **large-scale sorting**: Within each 1-minute bucket, sort the records by `sensor_id` in ascending order.
5. **Feature extraction**: Calculate the maximum and minimum `temperature` for each bucket.
6. **Template-based generation**: Every time a bucket is finalized (i.e., a log with a timestamp in the next minute arrives), generate an HTML report and write it to `/home/user/reports/index.html`. 

The HTML report must follow this exact template structure:
```html
<html>
<head><title>Telemetry Report</title></head>
<body>
<h1>Bucket: [Bucket Start Timestamp]</h1>
<p>Max Temp: [Max], Min Temp: [Min]</p>
<ul>
<li>Sensor [sensor_id]: [temperature] - [metadata]</li>
<!-- ... sorted list of all valid events in this bucket ... -->
</ul>
</body>
</html>
```

### Constraints
- Do not use root privileges (`sudo`).
- Compile your C code with standard GCC flags (e.g., `gcc -O2 processor.c -o log_tool -lhiredis`).
- Leave the compiled `log_tool` executable in `/home/user/`.