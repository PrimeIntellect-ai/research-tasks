You are a build engineer managing a distributed artifact caching and resolution system. We are migrating our internal build dependency graph resolution to a gRPC service with a WebSocket streaming frontend, but our current Python prototype has severe memory leaks and lacks the required network interfaces.

Your objective is to fix the memory leak, define the gRPC interface, and implement a combined gRPC/WebSocket server.

Phase 1: Fix the Memory Leak
In `/home/user/artifact_graph.py` (which already exists), there is a custom data structure representing build artifacts as a Directed Acyclic Graph (DAG). It correctly computes the topological build order. However, it crashes our system in long-running jobs because of a memory leak caused by circular references (nodes hold references to their dependencies, and dependencies hold "dependent_on" references back to their parents).
1. Use a memory profiler to identify the leak.
2. Fix the `artifact_graph.py` file so that it no longer leaks memory. You must not change the API of the `BuildGraph` class, only internal references (e.g., using `weakref` or explicitly breaking cycles).
3. Write a brief explanation of the fix to `/home/user/memory_fix_log.txt`.

Phase 2: Protobuf Definition
Create a protobuf file at `/home/user/build_service.proto` with the following specification:
- `syntax = "proto3";`
- A message `Artifact` with fields: `string name = 1;` and `repeated string depends_on = 2;`
- A message `GraphRequest` with field: `repeated Artifact artifacts = 1;`
- A message `OrderResponse` with field: `repeated string build_order = 1;`
- A service `BuildResolver` with an RPC `Resolve` that takes a `GraphRequest` and returns an `OrderResponse`.
Compile this protobuf into Python files in `/home/user/`.

Phase 3: Service Implementation
Create a Python script at `/home/user/server.py` that imports `artifact_graph.py` and the compiled protobufs. It must do the following concurrently (e.g., using `asyncio`):
1. Start a gRPC server on `localhost:50051`. The `Resolve` method must parse the request, feed the artifacts and dependencies into `artifact_graph.BuildGraph`, call its `get_build_order()` method, and return the `OrderResponse`. If a cycle is detected, return an empty `build_order`.
2. Start a WebSocket server on `localhost:8765`. When a client connects and sends a JSON string identical to the `GraphRequest` (e.g., `{"artifacts": [{"name": "A", "depends_on": []}, {"name": "B", "depends_on": ["A"]}]}`), parse it, compute the build order, and stream the build steps back over the websocket one by one as JSON: `{"step": "A"}`, then wait 0.1 seconds, then `{"step": "B"}`. Close the connection when done.

Finally, ensure your server script is executable and leave it running in the background as a daemon or background process so it can be tested: `python3 /home/user/server.py &`

Record the PID of the running server in `/home/user/server.pid`.