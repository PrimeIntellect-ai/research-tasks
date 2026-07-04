You are a DevOps engineer tasked with debugging and fixing a custom log processing pipeline. The system consists of three components:
1. A Redis instance acting as a message broker.
2. A TCP Log Ingestor (`/app/ingestor.py`) that receives JSON logs over TCP and queues them in Redis.
3. A Flask-based Log Processor (`/app/processor/app.py`) that reads logs from Redis, calculates an anomaly score using a high-performance C extension, and serves the results via an HTTP API.

Currently, the pipeline is completely broken. Your job is to fix the bugs, compile the extensions, and successfully start all services so they work together perfectly.

Here are the specific issues you need to resolve:

**1. Compiler and Linker Errors:**
The Log Processor uses a custom C extension located in `/app/processor/ext/` to calculate the Shannon entropy of log messages. However, trying to build it using `/app/processor/ext/setup.py` fails due to unresolved symbols (linker errors) and potentially a compilation issue. Fix `setup.py` and/or the C code so that it compiles successfully using `python3 setup.py build_ext --inplace`. 

**2. Formula Implementation Correction:**
The anomaly score is supposed to be the Shannon entropy of the character distribution in the log message. The C function `calculate_entropy` is mathematically incorrect. It currently calculates `sum += p * log(p)` (natural log), but the correct formula for Shannon entropy in bits is `H = - sum(p * log2(p))` (where p is the probability of a character, and log2 is the base-2 logarithm). Fix the C implementation so it computes the correct base-2 Shannon entropy.

**3. Corrupted Input Handling:**
The TCP Ingestor (`/app/ingestor.py`) crashes when it receives malformed JSON strings or corrupted byte streams. You must modify `/app/ingestor.py` so that:
- It catches JSON decoding errors and Unicode decoding errors.
- Instead of crashing or dropping the connection, it pushes the raw corrupted payload (as a UTF-8 string, replacing invalid characters with `?`) to a Redis list named `dead_letter`.
- Valid parsed JSON objects should continue to be pushed to the Redis list named `logs` as serialized JSON strings.

**Service Setup & Integration:**
Once the code is fixed, you must start the services. They must listen on the exact following local ports:
- Redis: Start using `redis-server /app/redis.conf` (listens on port `6379`).
- TCP Log Ingestor: Must listen on `127.0.0.1:5000`. (Run `python3 /app/ingestor.py`)
- HTTP Log Processor: Must listen on `127.0.0.1:8000`. (Run `cd /app/processor && gunicorn -b 127.0.0.1:8000 app:app` or similar).

Leave these three services running in the background. Our automated verifier will:
1. Connect to `127.0.0.1:5000` via TCP and send a mix of valid JSON logs and corrupted text payloads.
2. Query `http://127.0.0.1:8000/stats` to verify that the valid logs were processed, the anomaly scores match the corrected entropy formula, and the corrupted logs were properly routed to the dead letter queue.

**Environment details:**
- All code is located in `/app/`.
- Do not change the Redis configuration file (`/app/redis.conf`) or the ports.
- Ensure all services are up and running as your final state.