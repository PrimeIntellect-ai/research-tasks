You are a log analyst and data engineer investigating system patterns. Our log aggregation pipeline has broken down, and we need you to restore it by writing a high-performance Python processor that glues our infrastructure back together.

We have a multi-service architecture located in `/app/`. When the system starts, the following services are automatically brought up:
1. A Redis server running on `localhost:6379`.
2. A Log Emitter (`/app/emitter.py`) running in the background. It continuously generates logs and pushes them as JSON strings to a Redis list named `raw_logs`.
3. A Metrics API (`/app/api.py`) running on `localhost:8080`. It serves an endpoint `/metrics` that reads from a Redis Hash named `metrics:counts`.

Your task is to write a Python script at `/home/user/processor.py` and run it in the background to complete the ETL pipeline. It must perform the following:

1. **Extract and Parallel Process**: Continuously pop logs from the Redis list `raw_logs`. You must process these logs using multiple worker processes (e.g., Python's `multiprocessing` module) to handle the high throughput.
2. **Constraint-based Validation**: Each log is a JSON string. Parse and validate it. A valid log must contain exactly the following keys: `id`, `timestamp`, `service`, `level`, and `msg`. 
   - `id` must be a valid UUID4.
   - `level` must be one of `INFO`, `WARN`, or `CRITICAL`.
   - Any log failing these constraints must be discarded.
3. **Sorting, Grouping, and Aggregation**: Group the valid logs by `service` and `level`. For every valid log, increment a counter in the Redis Hash `metrics:counts` using the key format `<service>_<level>` (e.g., `payment-service_INFO`).
4. **Real-time Alerting (Stream Processing)**: Your processor must also start a TCP server listening on `localhost:9000`. Whenever a valid log with the level `CRITICAL` is processed, your TCP server must immediately broadcast the raw valid JSON string (exactly as it was received, followed by a newline `\n`) to all currently connected TCP clients.

Ensure your `processor.py` is running and all services are connected. We will verify the system by checking the aggregated stats via the HTTP API on port 8080 and by connecting a raw TCP client to port 9000 to listen for CRITICAL log alerts.