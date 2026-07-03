Wake up, you're the on-call engineer and just got paged at 3:00 AM. Our critical "SensorGrid" telemetry processing pipeline has completely collapsed under the new traffic load. The system is dropping data, crashing intermittently, and the final telemetry aggregates are wildly inaccurate. 

The system consists of three interacting components located in `/app/`:
1. **Redis Server**: Acts as our message broker and state store (Port 6379).
2. **Ingest Service** (`/app/ingest_service.py`): A Python TCP server (Port 8000) that receives raw byte streams of telemetry from field sensors, deserializes them, and queues them into Redis (list `sensor_queue`).
3. **Worker Pool** (`/app/worker_service.py`): A multi-process Python worker that pulls items from `sensor_queue`, parses the sensor values, and updates a global accumulator in Redis (key `global_accumulator`).

There are multiple critical bugs you must diagnose and fix:
1. **Encoding/Serialization Troubleshooting**: Some legacy sensors send data encoded in `Windows-1252` instead of `UTF-8`. The Ingest Service crashes trying to decode these byte streams, dropping the connection. You must modify `/app/ingest_service.py` to gracefully handle and decode `Windows-1252` payloads when standard UTF-8 decoding fails.
2. **Concurrency/Race Conditions**: The workers are dropping updates. They read the `global_accumulator`, add the new value, and write it back. Under high concurrency, this read-modify-write cycle is suffering from severe race conditions. You must fix the concurrency issue in `/app/worker_service.py` using Redis transactions (WATCH/MULTI/EXEC) or atomic operations.
3. **Floating-Point Precision Repair**: The telemetry values are extremely small floating-point deltas (e.g., $10^{-12}$). Simply adding them to a large running total is causing catastrophic loss of significance. Modify the worker to use a precision-safe accumulation method (e.g., maintaining the accumulator using Python's `decimal` module with high precision, or formatting it safely).

**Your Goal:**
1. Start the Redis server (e.g., `redis-server --daemonize yes`).
2. Start the Ingest Service and Worker Pool in the background.
3. Fix the bugs in `/app/ingest_service.py` and `/app/worker_service.py`.
4. Run the end-to-end integration test: `python3 /app/test_flow.py`.

The `test_flow.py` script will blast the Ingest Service with 15,000 sensor readings (some with legacy encoding, all with tiny float deltas) across multiple threads. It will then fetch the `global_accumulator` from Redis and write the final float value to `/home/user/final_result.txt`.

You are finished when `/home/user/final_result.txt` contains the correct aggregate sum. An automated verifier will read this file and compare your result against the mathematically true sum. To pass, the absolute error must be less than $10^{-8}$.