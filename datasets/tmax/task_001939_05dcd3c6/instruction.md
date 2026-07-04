You are an open-source maintainer reviewing a pull request for a mathematical execution engine repository located at `/home/user/math_dag`. 

The project uses a gRPC service to accept a Directed Acyclic Graph (DAG) of mathematical operations, topologically sorts them to determine the execution order, and translates them into a minimal sequential instruction set. 

The author of the PR attempted to optimize the build system and the topological sort algorithm, but broke several things. Your task is to fix the PR.

Here is what you need to do:
1. **Fix the Build**: The `Makefile` in `/home/user/math_dag` is supposed to compile the protobuf definition (`math_graph.proto`) into Python gRPC stubs. However, the PR author mangled the `protoc` command in the `build` target. Fix the `Makefile` so that running `make build` successfully generates `math_graph_pb2.py` and `math_graph_pb2_grpc.py`. (Hint: Use `python3 -m grpc_tools.protoc`).
2. **Fix the Graph Traversal**: The gRPC server in `server.py` implements Kahn's algorithm for topological sorting in the `Compile` RPC method. The PR author made a logical error in how dependencies (in-degrees) are updated, causing the mathematical operations to be evaluated in the wrong order or causing a cycle exception. Identify and fix the bug in `server.py`.
3. **Verify**: The project includes a `client.py` that sends a complex mathematical graph to the server and writes the resulting sequential instructions to `output.txt`. 
4. **Final Step**: Once you have fixed the build and the server code, run the following commands to test it:
   - Run `make build`
   - Start the server in the background: `python3 server.py &`
   - Wait a moment, then run the client: `python3 client.py`
   - Use standard shell tools to diff the generated `output.txt` against the provided `expected.txt` in unified diff format. Save the diff to `/home/user/math_dag/diff_result.txt`. If your fixes are correct, the diff should be empty.

Your final success will be measured by a correct `server.py` implementation, successful stub generation, and an empty `/home/user/math_dag/diff_result.txt`.