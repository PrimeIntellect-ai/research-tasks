You are a data engineer tasked with building a real-time ETL pipeline that processes complex log data, extracts structured metrics, and serves the results. 

We have a multi-service setup. Under `/app/`, there is a `start_services.sh` script that starts a local Redis server on port 6379 and an Nginx instance on port 8080. Nginx is configured to reverse-proxy requests to `127.0.0.1:9000`.

Your objective is to:
1. Write a C++ HTTP server listening on port 9000 using the header-only library available at `/home/user/cpp-httplib/httplib.h`.
2. Expose a POST endpoint at `/ingest` that receives CSV data. The CSV has three columns: `machine_id`, `timestamp`, and `sensor_dump`. The `sensor_dump` column is enclosed in double quotes and often contains embedded newlines and unstructured text.
3. In your C++ program, safely parse this CSV (taking care to handle embedded newlines within quotes without dropping rows). 
4. Use C++ regular expressions to extract structured information from the `sensor_dump` text. Specifically, look for patterns like `Temp: <value>C`, `Load: <value>%`, and `Fan: <value>RPM`.
5. Reshape this wide data into a long format. For each successfully parsed row, construct multiple long-format JSON objects, e.g., `{"machine_id": "m1", "timestamp": "2023-10-01T12:00:00Z", "metric": "Temp", "value": "45"}`.
6. Push these JSON objects as strings into a Redis list named `pipeline_metrics` using standard TCP commands to `127.0.0.1:6379` (or by invoking `redis-cli` from your C++ code).
7. Return a 200 OK HTTP response with the total number of metrics extracted.

Additionally, you must handle pipeline scheduling:
8. Create a shell script at `/home/user/flush_metrics.sh` that pops all items from the Redis list `pipeline_metrics` and appends them to `/home/user/data/metrics_archive.jsonl`.
9. Set up a user-level cron job that runs `/home/user/flush_metrics.sh` every minute.

Ensure your C++ server is compiled and running in the background. The verification suite will interact with your pipeline through the Nginx proxy on port 8080, sending malicious and normal CSV payloads, and will verify both the Redis state and the cron-generated archive files.