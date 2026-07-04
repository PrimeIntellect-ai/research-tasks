You have inherited an unfamiliar, partially broken data processing pipeline. The system receives sensor telemetry, queues it, and processes it to calculate running statistics.

The system consists of:
1. A Python Flask gateway (`/home/user/workspace/gateway.py`) that receives JSON data, serializes it to a binary format, and queues it in Redis.
2. A Redis server (running locally on default port 6379).
3. A C++ worker (`/home/user/workspace/worker.cpp`) that reads the binary data from Redis, decodes it, and calculates the sample variance of the readings for each sensor.

Unfortunately, the pipeline is failing in several ways:
1. **Service Disconnect:** The data sent to the gateway never seems to be processed by the worker. There is a configuration or wiring mismatch between the gateway and the worker.
2. **Decoding Errors:** When the worker does receive data, it misinterprets the binary payload due to a serialization/encoding bug. The Python gateway packs a 1-byte sensor ID, a 4-byte integer timestamp, and a 4-byte float32 reading. The C++ worker is reading garbage values.
3. **Numerical Instability:** The variance calculation in the C++ worker uses a naive formula (`(sum_sq - (sum*sum)/N) / (N-1)`). For our sensor data (which has small fluctuations around a very large mean), this causes catastrophic cancellation and outputs `0.0` or erratic values. 

Your tasks:
1. Identify and fix the communication mismatch between `gateway.py` and `worker.cpp` so they use the same Redis list. Modify whichever file makes more sense to align them.
2. Fix the struct padding/serialization issue in `worker.cpp` so it correctly reads the 9-byte payloads.
3. Replace the naive variance calculation in `worker.cpp` with Welford's online algorithm to ensure numerical stability.
4. Compile your fixed C++ worker to `/home/user/workspace/worker_fixed`.

To help you with the C++ fixes, we have provided a stripped reference binary at `/opt/oracle/worker_oracle`. Your compiled `/home/user/workspace/worker_fixed` must exhibit **bit-exact equivalence** to the oracle. Both the oracle and your worker support a CLI mode for easy testing: `./worker --file-mode <input.bin> <output.bin>`. The verification system will random-fuzz your C++ program in file mode to ensure it perfectly matches the oracle's output.

Finally, ensure the end-to-end pipeline works. You can start the gateway and test it by sending POST requests to `http://127.0.0.1:5000/ingest` with JSON like `{"sensor_id": 2, "timestamp": 1620000000, "value": 1000000.005}`. The worker should pull this, process it, and push the resulting variance to a Redis list named `processed_variances`.

Please leave your corrected C++ source in `/home/user/workspace/worker.cpp` and the compiled executable at `/home/user/workspace/worker_fixed`. Make sure `gateway.py` is also updated if you chose to fix the configuration there.