You are a performance engineer tasked with debugging and fixing a telemetry aggregation pipeline located in `/app/`.

The pipeline consists of three services:
1. A Redis instance (standard data store).
2. A C++ Telemetry Aggregator (`/app/aggregator/`) that ingests raw metrics over a custom TCP protocol and serves aggregated stats.
3. A Python HTTP Dashboard (`/app/dashboard/`) that provides a REST API to query the aggregated metrics.

Currently, the system is broken and failing under load:
1. **Crash Analysis**: The C++ aggregator intermittently crashed in production. A recent core dump is located at `/app/core/core.aggregator`. You must extract the malformed "poison pill" telemetry string that caused the crash. Write this exact string to `/home/user/poison_pill.txt`.
2. **Race Condition & Bottleneck**: The C++ aggregator (`/app/aggregator/src/server.cpp`) suffers from a severe race condition during concurrent metric ingestion, causing deadlocks. Furthermore, profiling reveals a severe performance bottleneck caused by synchronous, blocking system calls within the critical section. Fix the C++ code to eliminate the deadlock, ensure thread-safe metric aggregation, and remove the bottleneck so it can handle concurrent ingestion without blocking on file I/O.
3. **Service Composition**: The services are not configured to communicate correctly. Update `/app/dashboard/config.json` and `/app/aggregator/config.ini` so that:
   - Redis runs on `127.0.0.1:6379`.
   - The C++ aggregator listens for TCP ingestion on `127.0.0.1:8080` and for internal queries on `127.0.0.1:8081`.
   - The Python dashboard listens for HTTP traffic on `127.0.0.1:9000` and correctly queries the C++ aggregator.

Once you have fixed the C++ code and configuration files, compile the C++ aggregator using the provided `Makefile` in `/app/aggregator/` and start all three services. You can use the `start_all.sh` script provided in `/app/` to launch them in the background.

The final system must be running and able to handle concurrent TCP connections to `127.0.0.1:8080` sending `AUTH:DEVICE:VALUE\n` payloads, and HTTP GET requests to `http://127.0.0.1:9000/api/stats` returning the correct JSON aggregations. Do not change the overall architecture or the API response formats.