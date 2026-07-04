You are a platform engineer building a real-time log streaming tool for our new CI/CD pipeline infrastructure. 

Currently, CI/CD runners report their statuses via gRPC, but our frontend dashboard requires WebSockets. You need to build a lightweight Python bridge that receives gRPC messages and broadcasts them over WebSockets, and then write a pipeline integration test for it.

I have placed a protocol buffer definition at `/home/user/monitor.proto` with the following content:
```proto
syntax = "proto3";

package monitor;

message LogMessage {
  string level = 1;
  string payload = 2;
}

message Empty {}

service PipelineMonitor {
  rpc BroadcastLog (LogMessage) returns (Empty) {}
}
```

Your task:
1. Generate the Python gRPC code from `/home/user/monitor.proto`. You can use the `grpcio-tools` package.
2. Create a Python script at `/home/user/bridge.py` that:
   - Starts an asynchronous gRPC server listening on `localhost:50051`.
   - Starts a WebSocket server listening on `localhost:8765`.
   - Implements the `PipelineMonitor` service. When `BroadcastLog` is called, it should take the `payload` string and broadcast it to all currently connected WebSocket clients.
3. Create a shell script at `/home/user/test_pipeline.sh` that performs an automated integration test (simulating a CI pipeline run):
   - Starts `/home/user/bridge.py` in the background.
   - Starts a WebSocket client (you can use python inline or a separate script) that connects to `ws://localhost:8765`, waits for exactly ONE message, writes the message text to `/home/user/dashboard_output.log`, and disconnects.
   - Runs a gRPC client that calls `BroadcastLog` with `level="INFO"` and `payload="CI_BUILD_SUCCESS"`.
   - Cleans up and kills the background `bridge.py` process before exiting.

Requirements:
- Ensure the `grpcio`, `grpcio-tools`, and `websockets` Python packages are installed.
- When `/home/user/test_pipeline.sh` is executed, it must eventually produce `/home/user/dashboard_output.log` containing exactly the text `CI_BUILD_SUCCESS`.
- Make sure `/home/user/test_pipeline.sh` is executable (`chmod +x`).