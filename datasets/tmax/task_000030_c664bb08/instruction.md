You are an engineer tasked with porting an internal telemetry bridge to work in a minimal, scratch-like Linux container. 

We have a legacy system that emits telemetry via a gRPC stream. However, our new web dashboard requires a WebSocket endpoint. Your task is to build a C++ application that acts as a bridge: it must act as a gRPC client to consume the telemetry stream, and simultaneously run a WebSocket server to broadcast the telemetry data as JSON to all connected clients. Finally, you must write a packaging script that simulates a CI/CD step to gather the compiled binary and its dynamic dependencies into a distribution folder for containerization.

Here are the requirements:

1. **Protobuf Definition (`/home/user/project/telemetry.proto`):**
   Create a gRPC service named `TelemetryService` in the `telemetry` package. 
   It should have an RPC method `StreamMetrics` that takes an empty message `EmptyRequest` and returns a stream of `Metric` messages.
   A `Metric` message should have two fields: `string name = 1;` and `double value = 2;`.

2. **C++ Bridge Implementation (`/home/user/project/bridge.cpp`):**
   Write a C++ program that:
   - Connects to a gRPC server at `localhost:50051`.
   - Calls the `StreamMetrics` RPC.
   - Runs a WebSocket server on port `8080` (you can use the header-only `websocketpp` library with `asio`).
   - For every `Metric` received from the gRPC stream, it broadcasts a JSON string `{"name": "<name>", "value": <value>}` to all currently connected WebSocket clients.
   *(Note: Ensure your WebSocket server runs on a separate thread or uses async I/O so it doesn't block the gRPC stream reading, or vice versa).*

3. **Build System (`/home/user/project/CMakeLists.txt`):**
   Create a CMake configuration to build an executable named `telemetry_bridge`. It must link against gRPC, Protobuf, and any required Boost/pthread libraries for `websocketpp`.

4. **CI/CD Packaging Script (`/home/user/project/build_and_package.sh`):**
   Write a bash script that:
   - Builds the project in `/home/user/project/build`.
   - Creates a minimal filesystem tree at `/home/user/dist` (with `/home/user/dist/bin` and `/home/user/dist/lib`).
   - Copies the `telemetry_bridge` executable to `/home/user/dist/bin/`.
   - Uses `ldd` to find all dynamic shared library dependencies of the executable and copies them into `/home/user/dist/lib/` (ignore `linux-vdso.so`).

Ensure your script is executable (`chmod +x build_and_package.sh`). When the automated system tests your solution, it will run your script, start a mock gRPC server, run the packaged binary from `/home/user/dist/bin/telemetry_bridge` using `LD_LIBRARY_PATH=/home/user/dist/lib`, and connect a WebSocket client to verify the JSON data stream.