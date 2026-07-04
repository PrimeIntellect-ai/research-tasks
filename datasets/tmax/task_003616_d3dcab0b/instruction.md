You are a script developer responsible for modernizing a legacy graph-processing tool. We have a compiled, stripped legacy binary located at `/app/graph_oracle` that computes the critical path (maximum weight path) of a Directed Acyclic Graph (DAG), but we lost the source code. 

Your task is to reverse-engineer its behavior and create a modernized, high-performance C/C++ shared library with a Python wrapper.

Here is what you need to do:

1. **Analyze the Oracle & Patch File:**
   - The binary `/app/graph_oracle` takes a single file path as an argument. The file contains graph definitions.
   - We recovered an old patch file `/app/parser_fix.patch`. Apply your diff/patch analysis skills to understand how comments and edge cases are parsed in the graph text format.
   - You can also interact with `/app/graph_oracle` directly (black-box testing) to infer its output format and behavior.

2. **Implement the Core Logic (Shared Library):**
   - Write a C or C++ implementation of the graph traversal and dependency resolution logic.
   - Compile it into a shared library at `/home/user/libgraph.so`.
   - Your shared library must expose a C-ABI compliant function: `long calculate_critical_path(const char* graph_data);`. 
   - Note: The input to this function is the raw string content of the graph file, NOT the file path. It must parse the string, resolve the DAG dependencies to find the path with the maximum sum of node weights, and return that maximum integer weight.

3. **Develop the Python CLI:**
   - Write a Python script at `/home/user/cli.py`.
   - It must use `ctypes` to load `/home/user/libgraph.so` and call `calculate_critical_path`.
   - The CLI should accept exactly one positional argument: the path to an input text file.
   - It must print the exact same output format as `/app/graph_oracle` to standard output.

4. **Performance Benchmark:**
   - The new implementation must be highly performant. A script `/app/bench.py` is provided. Run it to ensure your C/C++ implementation completes the stress tests faster than the legacy binary.

Ensure your Python wrapper's output perfectly matches the legacy binary for any valid DAG input, as it will be subjected to an equivalence fuzzer.