You are an integration developer testing a new data processing pipeline. We have a set of mock API responses representing service tasks and their dependencies, but our high-performance graph resolution library is crashing during testing. 

Your objective is to fix the memory safety issue in our C library, compile it, and write a Python script that parses the API data, interfaces with the C library to resolve the dependency graph, and produces an execution plan.

Here are the details:
1. **API Responses**: Located in `/home/user/api_responses/`. Each file is a JSON representing a task. It contains an `"id"` (string) and a `"requires"` (list of string IDs) field.
2. **C Library**: Located at `/home/user/libgraph.c`. It contains a function `int* resolve_dependencies(int num_nodes, int num_edges, int* edge_u, int* edge_v)` which performs a topological sort. 
   - *Issue*: The library has a memory safety bug (buffer overflow) that causes a segmentation fault on larger graphs because it writes a sentinel value `-1` at the end of the `result` array but does not allocate enough memory for it. 
   - *Fix*: Modify `/home/user/libgraph.c` to allocate enough memory to safely store the sentinel value.
   - *Compile*: Compile it to a shared object `/home/user/libgraph.so` using `gcc -shared -o libgraph.so -fPIC libgraph.c`.
3. **Python Integration Test**: Write a script `/home/user/integration_test.py` that:
   - Parses all JSON files in `/home/user/api_responses/`.
   - Creates a mapping from the string IDs to integers (0 to N-1). **The integer mapping MUST be assigned by sorting the unique task IDs alphabetically** (e.g., if IDs are TaskA, TaskB, TaskC, they become 0, 1, 2).
   - Extracts all edges. An edge from U to V means V requires U (so U must execute before V). The `edge_u` array should contain the dependencies (sources), and `edge_v` should contain the dependent tasks (destinations).
   - Loads `/home/user/libgraph.so` using Python's `ctypes` module.
   - Calls `resolve_dependencies` with the correct arguments.
   - Reads the returned array up to the `-1` sentinel.
   - Maps the returned integers back to their string IDs.
   - Writes the resolved sequence of string IDs as a single comma-separated line to `/home/user/execution_plan.log` (e.g., `TaskA,TaskC,TaskB`).

Ensure your Python script runs without errors and creates the `execution_plan.log` file correctly.