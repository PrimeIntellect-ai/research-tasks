You are tasked with fixing a multi-file Python project located in `/home/user/graph_service` that currently fails to run due to both protobuf compilation errors and an algorithmic bug in the core logic. 

The project implements a gRPC service that takes a directed graph and returns its topological sort. 

Here is what you need to do:
1. **Fix the Protobuf Definition:** The file `/home/user/graph_service/graph.proto` contains syntax errors. Fix it so it properly defines a service `GraphService` with an rpc `TopologicalSort` that takes a `GraphRequest` and returns a `GraphResponse`.
2. **Compile the Protobuf:** Use `grpcio-tools` to generate the Python gRPC stubs (`graph_pb2.py` and `graph_pb2_grpc.py`) in the `/home/user/graph_service` directory.
3. **Fix the Algorithm:** The server implementation in `/home/user/graph_service/server.py` has a bug in its topological sorting algorithm. Fix it. The topological sort must be deterministic: whenever multiple nodes have an in-degree of 0, you **must break ties by picking the node with the smallest integer ID first**.
4. **Write an End-to-End Test:** Create a test script `/home/user/graph_service/test_e2e.py` that:
   - Starts the gRPC server.
   - Connects to the server locally on port `50051`.
   - Sends a request with the following directed edges: `(1->2), (2->3), (4->3), (5->6)`.
   - Receives the sorted node list and writes it as a comma-separated string (e.g., `1, 2, 3...`) to `/home/user/graph_service/result.txt`.
   - Gracefully shuts down the server.

You may need to install `grpcio` and `grpcio-tools` via pip to complete this task. Run your test script to generate the final `result.txt`.