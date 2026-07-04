You are an engineer tasked with porting an older mathematical dependency resolution tool to run as a microservice in a minimal container. You need to design a gRPC service that takes a directed acyclic graph (DAG) of mathematical operations, traverses it to resolve dependencies, calculates the values, and returns the result. You also need to perform a version compatibility check before running the service.

Your objective spans multiple phases:

Phase 1: Version Compatibility Check
1. Read the file `/home/user/config.json` (you will need to create a mock one for your own testing, but assume it exists in production). For this task, assume its contents are `{"engine_version": "1.7.4"}`.
2. Write a Python script `/home/user/version_check.py` that reads `/home/user/config.json`. The script should exit with code 0 if the `engine_version` is semantically greater than or equal to `1.5.0` and strictly less than `2.0.0`. Otherwise, it should exit with code 1. 

Phase 2: gRPC Protocol Design
1. Create a protobuf file at `/home/user/math_port/math_dag.proto` with `syntax = "proto3";`.
2. Define a service named `MathResolver`.
3. Define an RPC named `ResolveGraph` that takes a `GraphRequest` and returns a `GraphResponse`.
4. A `GraphRequest` contains a repeated `Node` field named `nodes`.
5. A `Node` message should have:
   - `string id` (e.g., "N1")
   - `string operation` (Can be "VALUE", "ADD", or "MULTIPLY")
   - `double value` (Used only if operation is "VALUE")
   - `repeated string dependencies` (List of node IDs this node depends on. For "ADD" or "MULTIPLY", this specifies the operands).
6. A `GraphResponse` contains a map `<string, double>` named `results` mapping node IDs to their fully evaluated numerical values.
7. Compile this protobuf file into Python using `grpcio-tools`. Output the compiled files into `/home/user/math_port/`.

Phase 3: Service Implementation
1. Write the Python server `/home/user/math_port/server.py`.
2. The server must implement the `MathResolver` service.
3. Upon receiving a `GraphRequest`, it must perform a topological sort / graph traversal to resolve the dependencies.
4. It must compute the mathematical result for each node:
   - "VALUE": Just the `value`.
   - "ADD": Sum of the evaluated dependencies.
   - "MULTIPLY": Product of the evaluated dependencies.
5. The server should listen on port `50051`.

Phase 4: Client Execution and Output
1. Write a Python client `/home/user/math_port/client.py` that connects to `localhost:50051`.
2. Construct the following graph in the client:
   - Node "A": VALUE = 3.5
   - Node "B": VALUE = 2.0
   - Node "C": ADD, dependencies = ["A", "B"]
   - Node "D": MULTIPLY, dependencies = ["C", "A"]
   - Node "E": ADD, dependencies = ["D", "B"]
3. Call the `ResolveGraph` RPC.
4. Serialize the returned `results` map to a JSON file at `/home/user/result.json` with keys sorted alphabetically. Format it as a flat JSON object (e.g., `{"A": 3.5, ...}`).

Ensure all scripts are executable. You can test your service by running the server in the background and executing the client. Ensure the final evaluated values are perfectly accurate.