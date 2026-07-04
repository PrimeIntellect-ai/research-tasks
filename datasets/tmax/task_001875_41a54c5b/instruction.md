You are a systems programmer debugging an integration issue in a custom dependency resolution tool. 

The tool has a C library backend for high-performance graph traversal, but the Python frontend is failing to load it due to a C library linking issue. Furthermore, the Python frontend parser hasn't been implemented yet.

Your workspace is located at `/home/user/sys_debug`. In this directory, you will find:
1. `Makefile` - Builds the C libraries.
2. `matrix.c` and `graph.c` - Source files for the graph traversal backend.
3. `graph.h` - Header file defining the ABI.
4. `graph_def.txt` - A custom text format describing a dependency graph.

Your task consists of the following steps:

**Phase 1: Fix the Linking Issue**
If you run `make` in `/home/user/sys_debug`, it will produce `libmatrix.so` and `libgraph.so`. However, attempting to load `libgraph.so` in Python via `ctypes` fails because `libgraph.so` uses functions from `libmatrix.so` but isn't properly linked against it, leading to undefined symbols. 
Modify the `Makefile` or build commands so that `libgraph.so` correctly links against `libmatrix.so` and can be loaded successfully by Python using `ctypes.CDLL('/home/user/sys_debug/libgraph.so')`.

**Phase 2: State Machine Parser & FFI Integration**
Write a Python script `/home/user/sys_debug/solver.py` that does the following:
1. Uses a state machine pattern to parse `graph_def.txt`. The file defines dependencies in blocks:
   ```
   NODE <node_id>
   DEPENDS <other_node_id>
   DEPENDS <other_node_id>
   END
   ```
   *Note: `<node_id>` are integers.*
2. Uses Python's `ctypes` module to interface with the C libraries. You must define the correct argument types and return types based on `graph.h`.
3. Calls the C functions to build the graph:
   - Call `init_graph(num_nodes)` (Assume maximum node ID + 1 is the number of nodes).
   - For each dependency parsed, call `add_edge(node_id, depends_on_id)`.
4. Executes the graph traversal by calling `traverse_and_count(start_node)`. Start the traversal from node `0`.
5. Logs the integer result returned by `traverse_and_count(0)` to a file named `/home/user/sys_debug/output.log`.

**Output Specification:**
The file `/home/user/sys_debug/output.log` must contain exactly one line with the integer result of the graph traversal.