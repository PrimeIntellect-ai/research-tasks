You are acting as a Release Manager preparing a new deployment pipeline monitoring system. We are migrating our deployment health scoring from a legacy Node.js microservice to a unified Python stack. The new system will ingest telemetry via gRPC, compute health scores using a translated algorithm, and broadcast critical deployment alerts in real-time via WebSockets.

Your task is to implement and orchestrate this system.

**Phase 1: Code Translation & Custom Data Structure**
You have been provided a legacy JavaScript file at `/home/user/legacy/scorer.js`. It contains a custom circular buffer data structure `ReadinessScorer` used to calculate a rolling deployment health score.
1. Translate this JavaScript class exactly into Python and save it as `/home/user/scorer.py`. The behavior and logic must remain identical.

**Phase 2: Protobuf Definition & Compilation**
1. Create a Protobuf file at `/home/user/deployment.proto` with:
   - `syntax = "proto3";`
   - A message `Metric`: containing `string service_name` and `int32 health_value`.
   - A message `DeployResponse`: containing `bool approved`.
   - A service `ReleaseManager` with an RPC `SendMetric` that takes a `Metric` and returns a `DeployResponse`.
2. Compile this proto file into Python using `grpc_tools.protoc` in the `/home/user/` directory.

**Phase 3: Service Implementation (gRPC + WebSockets)**
Write the server script at `/home/user/server.py`. The server must:
1. Start a gRPC server on `localhost:50051` implementing `ReleaseManager`.
2. Concurrently run a WebSocket server on `localhost:8765`.
3. Maintain a single instance of `ReadinessScorer` with a `window_size` of 3.
4. When `SendMetric` is called, pass `health_value` into the `ReadinessScorer.add_metric()` method.
5. Retrieve the score via `get_score()`. If the score drops below `50`, the RPC should return `approved = False`. Otherwise, `approved = True`.
6. Whenever a score drops below `50`, immediately broadcast a JSON message over the WebSocket to all connected clients. The format must be exactly: `{"alert": "deployment halted", "service": "<service_name>", "score": <calculated_score>}`.

**Phase 4: End-to-End Orchestration**
We have provided a gRPC client `/home/user/tests/grpc_client.py` and a WebSocket listener `/home/user/tests/ws_listener.py`. 
Write a bash script at `/home/user/run_e2e.sh` that:
1. Starts `server.py` in the background.
2. Waits 2 seconds for servers to initialize.
3. Starts `python /home/user/tests/ws_listener.py` in the background (it will automatically write received broadcasts to `/home/user/alerts.log`).
4. Runs `python /home/user/tests/grpc_client.py` (which sends a pre-defined sequence of metrics).
5. Waits for the grpc_client to finish.
6. Gracefully terminates the background processes (both `server.py` and `ws_listener.py`).
7. Exits with code 0.

Ensure your orchestration script creates the `/home/user/alerts.log` file indirectly by successfully orchestrating the test.