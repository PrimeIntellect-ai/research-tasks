You are a build engineer architecting a real-time artifact telemetry pipeline. You need to implement and benchmark a system that streams build artifact metadata over WebSockets, parses it, transforms it, and measures processing performance. 

Your task is to write three files: a WebSocket server, a WebSocket client, and a shell script to orchestrate them.

**1. The WebSocket Server (`/home/user/ws_server.py`)**
Write a Python script using the `websockets` library that starts a server on `ws://127.0.0.1:8888`. 
When a client connects, the server must sequentially send exactly 10,000 JSON messages and then close the connection.
Each message must have the following structure:
```json
{
  "build_id": <integer_starting_from_1_to_10000>,
  "artifact": {
    "name": "build_bin_<build_id>.zip",
    "size_bytes": <random_integer_between_1000_and_50000>
  },
  "test_coverage": {
    "unit": <random_float_between_0_and_100>,
    "integration": <random_float_between_0_and_100>
  }
}
```

**2. The WebSocket Client (`/home/user/ws_client.py`)**
Write a Python script that:
- Connects to `ws://127.0.0.1:8888`.
- Starts a high-resolution timer upon receiving the first message.
- Receives all 10,000 messages until the server closes the connection.
- Parses the JSON data and transforms it into a flattened structure:
  ```json
  {
    "id": <build_id>,
    "filename": "<artifact.name>",
    "total_coverage": <test_coverage.unit + test_coverage.integration>
  }
  ```
- Stops the timer once the connection is closed.
- Writes the entire list of transformed objects as a JSON array to `/home/user/transformed_artifacts.json`.
- Writes the benchmark results to `/home/user/benchmark.log` in this exact string format:
  `Processed 10000 messages in [TIME] seconds. Throughput: [RATE] msgs/sec.` 
  (Replace [TIME] and [RATE] with the calculated floats rounded to 4 decimal places).

**3. The Orchestrator (`/home/user/run.sh`)**
Write a bash script that:
- Installs the `websockets` package via pip.
- Starts `ws_server.py` in the background.
- Waits for 2 seconds to ensure the server is ready.
- Runs `ws_client.py`.
- Kills the server process cleanly after the client finishes.

Ensure `/home/user/run.sh` is executable and execute it to generate the final artifacts (`transformed_artifacts.json` and `benchmark.log`).