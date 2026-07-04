You are a log analyst investigating intermittent attacks on our infrastructure. We have a multi-service stack running locally (Nginx, a mock backend API, and Redis). The services are started via the script `/app/start_services.sh`.

Nginx is configured to serve traffic on port 8080 and writes access logs in JSON format to `/var/log/nginx/access.log`. Each log line is a JSON object containing at least the fields `"status"` (integer) and `"bytes"` (integer).

Your task is to build a time-series log analyzer and set up an automated monitoring pipeline.

1. **C++ Detector**: Write a C++ program at `/home/user/detector.cpp` and compile it to `/home/user/detector`. 
   - It must read a stream of JSON log lines from `stdin` (one JSON object per line).
   - It must compute rolling statistics over a sliding window of the last 10 log entries.
   - It should detect an anomaly if, in ANY 10-entry rolling window:
     - The average `"bytes"` transferred is strictly greater than 10,000.
     - AND there are strictly more than 3 entries with a `"status"` code >= 400.
   - If an anomaly is detected at any point in the stream, the program should immediately exit with status code `1` (indicating an attack/evil stream).
   - If the end of the stream is reached without detecting any anomalies, the program should exit with status code `0` (indicating a clean stream).

2. **Cron Monitoring**: Write a bash script at `/home/user/monitor.sh` that extracts the last 100 lines from `/var/log/nginx/access.log`, pipes them to your `/home/user/detector`, and if the detector exits with status code 1, appends the exact string "ALERT DETECTED\n" to `/home/user/alerts.log`.
   - Schedule this script to run every minute using cron for the user `user`.

You are provided with historical log samples in `/app/corpus/clean/` and `/app/corpus/evil/` to test your C++ program. Your detector must correctly classify 100% of these files.

Ensure your C++ code is robust enough to handle large file streams efficiently without loading the entire file into memory. Standard C++17 features and lightweight bash scripting are expected.