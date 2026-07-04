You are acting as a systems programmer helping to debug and complete a polyglot Go/C project. 

The project is located at `/home/user/math_dag/`. It is supposed to parse a JSON file representing a Directed Acyclic Graph (DAG) of mathematical operations, evaluate the graph concurrently using Go goroutines, and perform the actual mathematical calculations using a custom C library (`libmathcore.so`).

However, the previous developer left the project in a broken state:
1. **Linking Issue:** The C library build script (`/home/user/math_dag/build.sh`) is broken. It fails to correctly compile all the C objects into the shared library, resulting in missing symbols when the Go application tries to run.
2. **Missing Go Implementation:** The main Go application (`/home/user/math_dag/main.go`) is incomplete. It needs to read `/home/user/math_dag/graph.json`, resolve the dependency graph, evaluate the nodes concurrently (waiting for a node's dependencies to finish before calculating it), and call the C functions via cgo.

Your tasks are:

**Phase 1: Fix the Build**
- Inspect and fix `/home/user/math_dag/build.sh`. It must compile `math_add.c` and `math_mul.c` into a single shared library named `libmathcore.so`. Make sure to use the correct compiler flags for position-independent code and shared libraries.
- Fix any broken `cgo` directives in `main.go` so it properly links against `libmathcore.so` in the current directory.

**Phase 2: Complete the Go Concurrency & Graph Traversal**
- Complete `/home/user/math_dag/main.go`. 
- Parse `/home/user/math_dag/graph.json`. The JSON contains a list of nodes. Each node has:
  - `id` (string): The node's unique identifier.
  - `type` (string): Either `"value"`, `"add"`, or `"mul"`.
  - `val` (float64): Only present if `type` is `"value"`.
  - `deps` (array of strings): Only present if `type` is `"add"` or `"mul"`. It always contains exactly two node IDs representing the left and right operands.
- Evaluate the graph concurrently. Use Go goroutines and channels to ensure that an `"add"` or `"mul"` node only computes once its dependencies in `deps` have been fully evaluated. 
- Use the C functions `op_add` and `op_mul` (provided in `math_core.h`) via cgo to perform the calculations.

**Phase 3: Output Results**
- Write the final evaluated value of *every* node to `/home/user/math_dag/results.json`.
- The format must be a flat JSON object mapping the node `id` to its evaluated `float64` value. For example: `{"Node1": 5.0, "Node2": 15.0}`.

**Constraints:**
- Do not hardcode the evaluation order; it must be resolved dynamically based on the DAG dependencies.
- You must use cgo and the provided C library for calculations.
- Ensure the Go program compiles and runs successfully: `LD_LIBRARY_PATH=. go run main.go`.