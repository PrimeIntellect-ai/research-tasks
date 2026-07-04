You are a data engineer tasked with building an ETL processor in C++ that integrates with a multi-service pipeline.

We have a streaming data pipeline consisting of:
1. A Redis data store holding metadata.
2. A raw data generator that writes JSON strings to a named pipe.
3. A data sink that reads processed JSON strings from another named pipe.

Your objective is to write a C++ program that reads from standard input, performs data imputation, joins with Redis metadata, calculates a similarity metric, and writes the result to standard output. Finally, you must configure and run the services to establish the end-to-end flow.

### 1. The C++ ETL Processor
Create a C++ program at `/home/user/processor.cpp` and compile it to `/home/user/processor`. You may use `hiredis` and `nlohmann/json` (assume they can be installed via package manager).

For each line of input from `stdin`:
- Parse the JSON object: `{"sensor_id": "S1", "readings": [1.0, null, 3.0, null, 5.0]}`.
- Connect to a local Redis server (127.0.0.1:6379). Query the string value at key `sensor:<sensor_id>`. This value is a JSON array of floats (e.g., `[1.0, 2.0, 3.0, 4.0, 5.0]`) representing the `target_vector`.
- **Imputation**: Replace any `null` values in the `readings` array using linear interpolation between the nearest valid numbers. If leading or trailing values are `null`, copy the nearest valid number (e.g., `[null, 2.0]` becomes `[2.0, 2.0]`).
- **Distance**: Compute the Euclidean distance between the fully imputed `readings` array and the `target_vector` from Redis. Both arrays will always be the same length.
- Print a JSON line to `stdout` with the result: `{"sensor_id": "S1", "distance": 0.0000}`. Format the distance to exactly 4 decimal places.

### 2. Multi-Service Pipeline Setup
- Start the local Redis server on port 6379.
- A script at `/app/init_redis.py` is provided to populate Redis. Run it.
- Create named pipes at `/tmp/input.pipe` and `/tmp/output.pipe`.
- The data generator script is at `/app/generator.py`. It writes to `/tmp/input.pipe`.
- The data sink script is at `/app/sink.py`. It reads from `/tmp/output.pipe` and verifies the pipeline.
- You must run your `/home/user/processor` such that it continuously reads from `/tmp/input.pipe` and writes to `/tmp/output.pipe`, while the generator and sink are running.

Ensure your compiled binary at `/home/user/processor` is bit-exact in its algorithmic behavior to a reference implementation, as it will be rigorously fuzzed with thousands of random inputs by our automated test suite.