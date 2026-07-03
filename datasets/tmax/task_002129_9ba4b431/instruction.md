I am a web developer trying to integrate a legacy graph processing module into our new Python backend. We have lost the original C++ source code for the graph resolver, but we still have a compiled Linux binary of it located at `/app/oracle_graph_parser`. It reads a custom binary serialized graph format from standard input and prints the resolution order to standard output. 

I started writing a Python package to replace it, using a C++ backend exposed via Python's C-API, but I got stuck. The project is located in `/home/user/graph_pkg`. Currently, the `setup.py` is broken and fails to build the extension. Moreover, the skeleton C++ code I started in `/home/user/graph_pkg/src/resolver.cpp` is empty, and my earlier attempts had massive memory leaks.

Your task:
1. Reverse-engineer the input and output formats of `/app/oracle_graph_parser`. You can feed it files and use standard tools like `xxd`, `strings`, or `objdump` to figure out how it expects the binary graph to be structured and how it formats its output. It performs a topological sort on a directed graph.
2. Complete the C++ implementation in `/home/user/graph_pkg/src/resolver.cpp`. It must parse the same binary format and implement the exact same graph dependency resolution logic.
3. Fix `/home/user/graph_pkg/setup.py` so that it successfully compiles the C++ code as a Python C extension named `_graph_resolver`.
4. Ensure there are no memory leaks when the Python extension is called (I've been using Valgrind to check).
5. Create a Python script `/home/user/solution/runner.py` that reads all binary data from `sys.stdin.buffer`, passes it to your compiled `_graph_resolver.resolve(data)` function, and prints the exact string result to stdout, matching the oracle binary perfectly.

The final entry point for verification will be:
`python3 /home/user/solution/runner.py`
It must behave identically to `/app/oracle_graph_parser` for any valid binary graph input.