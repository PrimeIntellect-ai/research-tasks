You are a DevOps engineer tasked with debugging a data processing pipeline that handles high-precision sensor logs. 

The system consists of a multi-service architecture located in `/app/`:
1. **Message Broker**: A local instance of `redis-server` (running on port 6379).
2. **Log Receiver**: A Flask application (`/app/receiver.py`) running on port 5000 that accepts POST requests containing JSON sensor logs and pushes them to a Redis queue (`sensor_queue`).
3. **Data Worker**: A Python worker (`/app/worker.py`) that pops logs from `sensor_queue`, parses them, and writes the results.

**The Problem:**
We are experiencing intermittent pipeline failures. The `worker.py` script occasionally crashes with exceptions (similar to a panic on `unwrap()` when encountering edge-case log data missing certain fields) and drops the connection. Additionally, downstream teams are reporting precision loss in the `sensor_reading` field for successfully processed logs. The values are slightly different from the raw logs. 

There is an oracle binary at `/app/oracle_processor` that implements the exact, correct processing logic but we cannot deploy it directly due to compatibility issues. 

**Your tasks:**
1. Start the backend services (Redis and the Flask receiver). You will find a `docker-compose.yml` or standard start script `/app/start_services.sh` to help you bring up the services.
2. Interactively debug the `worker.py` processing logic by sending test logs via `curl` to `http://localhost:5000/ingest` and observing the crashes and precision issues. Use tools like `strace` or standard Python debuggers (`pdb`) to trace how the worker fails.
3. Identify the root causes of the crashes (malformed data) and the precision loss (likely floating-point inaccuracies).
4. Create a standalone Python script at `/app/fixed_processor.py` that takes JSON lines from `stdin`, processes them, and prints the resulting JSON lines to `stdout`. 
   - Your script must perfectly replicate the behavior of `/app/oracle_processor`. 
   - It must handle missing fields exactly as the oracle does (either by dropping the log or applying a specific default, which you must deduce by testing the oracle).
   - It must preserve the exact numerical precision of the `sensor_reading` field (use Python's `decimal` module if necessary).

**Verification:**
Your script `/app/fixed_processor.py` will be tested using a fuzzing equivalence verifier against `/app/oracle_processor`. The verifier will generate thousands of random JSON logs (including edge cases), pipe them via `stdin` to both your script and the oracle, and assert that the `stdout` outputs are bit-exact matches. Ensure your script reads line-by-line from `sys.stdin` and outputs standard JSON to `sys.stdout`.