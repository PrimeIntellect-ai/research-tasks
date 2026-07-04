You are a log analyst investigating anomalous patterns in our upstream ETL pipelines. We have an ETL generator service that crashes periodically and retries, producing duplicate time-series log records. We need to process this stream in real-time, anonymize sensitive data, deduplicate records, and expose processing metrics.

Your task is to write a C++ daemon that acts as an intermediary processing node, and to configure a cron-based pipeline schedule.

Here are the requirements:

1. **Services and Integration**:
   - We have an ETL generator script located at `/app/start_generator.sh`. When run, it simulates the upstream ETL job by attempting to connect to `127.0.0.1:9000` via TCP and continuously streaming raw log lines.
   - You must write a C++ application (compile it to `/home/user/log_processor`) that listens for TCP connections on `127.0.0.1:9000`.

2. **Stream Processing (C++)**:
   - The incoming stream consists of newline-separated records with the format:
     `timestamp,record_id,user_ip,user_email,event_type,value`
   - Your C++ service must stream these records to a file at `/home/user/processed_logs.csv`.
   - **Data Masking**:
     - Replace the last octet of the `user_ip` with `XXX` (e.g., `192.168.1.50` -> `192.168.1.XXX`).
     - Redact the local part of the `user_email` with `***` (e.g., `alice.smith@example.com` -> `***@example.com`).
   - **Deduplication**:
     - The ETL system sends duplicate `record_id`s on retry. If you see a `record_id` you have already processed in the lifetime of the daemon, drop the record entirely (do not write it to the CSV).

3. **Multi-Protocol Metrics (C++)**:
   - Your C++ application must also run an HTTP server concurrently on `127.0.0.1:9001`.
   - We have provided a single-header HTTP library at `/app/include/httplib.h` which you can include in your C++ code.
   - When an HTTP `GET /stats` request is received, it must return a JSON response with the exact format:
     `{"unique": <count_of_unique_records_written>, "duplicates": <count_of_duplicates_dropped>}`
     Ensure the `Content-Type` is `application/json`.

4. **Pipeline Scheduling (Bash/Cron)**:
   - Create a directory `/home/user/archive`.
   - Write a bash script at `/home/user/rotate.sh` that safely copies `/home/user/processed_logs.csv` to `/home/user/archive/log_$(date +%s).csv` and then clears the contents of the original file (without deleting the file inode, e.g., using `>`).
   - Configure a cron job for the current user (`user`) to run `/home/user/rotate.sh` exactly every 1 minute.

Compile your C++ code using `g++ -std=c++17 -pthread -I/app/include log_processor.cpp -o /home/user/log_processor`. Start your C++ service in the background, then start `/app/start_generator.sh` in the background, and ensure the cron service is running. 

Do not use any external dependencies other than standard C++17 libraries, POSIX APIs, and the provided `httplib.h`.