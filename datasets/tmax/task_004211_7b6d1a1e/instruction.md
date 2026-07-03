We are migrating our legacy test orchestrator from Python 2 to Python 3. The old Python 2 orchestrator used a fragile C-extension to query module dependency graphs. As part of the migration, we are decoupling the architecture: you will write a Go microservice that wraps the legacy C graph library and exposes a WebSocket interface for the new Python 3 test runner.

The legacy C library is already compiled and located at `/home/user/legacy_c/libgraph.so` with its header at `/home/user/legacy_c/graph.h`.

The C header defines one function:
`int get_children(int node_id, int* out_children, int max_children);`
This function populates `out_children` with the immediate dependencies of `node_id` and returns the number of children found.

Your task is to:
1. Write a Go application at `/home/user/server.go` that uses `cgo` to link against `/home/user/legacy_c/libgraph.so`. 
2. The Go application must expose a WebSocket server on `ws://127.0.0.1:8080/ws`. (You may use `github.com/gorilla/websocket`).
3. When the server receives a JSON message in the format `{"target": <int>}`, it must:
   - Use the C function to perform a graph traversal (e.g., BFS or DFS) to find *all* reachable dependencies in the graph starting from the `target` node, including the `target` node itself.
   - You can assume a maximum of 100 children per node.
   - Return a JSON response `{"reachable": [<int>, <int>, ...]}` where the array contains all unique reachable node IDs, sorted in ascending order.
4. Write a Python 3 test script at `/home/user/test_ws.py` representing the new test runner. It must:
   - Connect to `ws://127.0.0.1:8080/ws`.
   - Send the message `{"target": 2}`.
   - Receive the response and write the `reachable` array as a comma-separated list of integers to `/home/user/migration_test.log` (e.g., `1,2,3`).

You will need to run the Go server in the background, run your Python 3 test script, and ensure the log file is created correctly. Ensure any necessary dependencies (like `gorilla/websocket` or Python's `websockets` package) are installed. Note: you may need to configure `LD_LIBRARY_PATH` when running your Go server.