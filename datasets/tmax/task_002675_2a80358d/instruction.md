You are a data analyst tasked with building a high-performance C pipeline to process a continuous stream of CSV log data. The system involves several interacting services that you must configure and tie together.

### Multi-Service Environment
The following services are available and need to be integrated:
1. **Redis**: Running on `127.0.0.1:6379`. It acts as a message queue. A background data producer is continuously pushing raw CSV strings to a Redis LIST named `raw_logs`.
2. **Nginx**: Running on `127.0.0.1:8080`. You must configure Nginx to serve static files from `/home/user/www/` on this port.

### Data Format
The CSV pushed to Redis has the following format:
`msg_id,timestamp,user_text,value`
Example: `a1b2c3d4e5f6g7h8,1678886400,Hello World,42.5`

### Task 1: Adversarial Sanitizer CLI
Some of the incoming logs are malformed or malicious. You must write a standalone C program at `/home/user/filter_cli` that takes two arguments: an input CSV file path and an output CSV file path (`/home/user/filter_cli <input> <output>`).
It must filter rows based on these strict rules:
1. `msg_id` must be exactly 16 hexadecimal characters.
2. `timestamp` must be a positive integer.
3. `user_text` must be at most 100 characters long and contain ONLY alphanumeric characters and spaces (no punctuation, no control characters, no invalid UTF-8).
4. `value` must be a parsable float.
Rows failing ANY of these conditions must be completely dropped. Valid rows must be written to the output file exactly as they appeared.

### Task 2: Live Processing Daemon
Write a C program at `/home/user/processor.c` (and compile it to `/home/user/processor`) that:
1. Connects to Redis and continuously blocks/pops (`BLPOP`) from the `raw_logs` list.
2. Applies the exact same sanitization rules as Task 1.
3. **Hash-based Deduplication**: Maintains an in-memory hash set of `msg_id`s. If a `msg_id` has been seen before, drop the row.
4. **Tokenization and Normalization**: Converts the valid `user_text` to strictly lowercase.
5. **Aggregation**: Maintains running summary statistics for valid, unique records:
   - `total_valid_records`
   - `sum_values`
   - `max_value`
6. After processing every 10 valid records, the daemon must write the current statistics to `/home/user/www/stats.json` in the following exact JSON format:
   `{"total_valid_records": X, "sum_values": Y.YY, "max_value": Z.ZZ}` (format floats to 2 decimal places).

Configure the services, write the code, start Nginx, and leave your `/home/user/processor` daemon running in the background. Note: you may install `libhiredis-dev` to connect to Redis.