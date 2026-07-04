You are an integration developer tasked with replacing a legacy Rust-based API orchestration service with a new Python implementation. 

The legacy service binary is located at `/app/graph_oracle`. It is a stripped, compiled executable. We no longer have its source code, but we know it processes a custom dependency graph text format from standard input (`stdin`) and outputs the resolved "critical path" of API calls to standard output (`stdout`).

Your objective is to reverse-engineer the behavior of `/app/graph_oracle` through black-box testing and create a Python script at `/home/user/graph_eval.py` that behaves identically (bit-exact) for all possible inputs.

From our outdated documentation, we know the input format consists of newline-separated directives:
1. `V <NodeID> <Latency>` - Defines an API endpoint and its execution time in milliseconds (e.g., `V FETCH_USER 45`). `<NodeID>` is an alphanumeric string. `<Latency>` is a positive integer.
2. `E <NodeID1> <NodeID2>` - Defines a directed dependency edge, meaning `<NodeID1>` must complete before `<NodeID2>` begins (e.g., `E FETCH_USER FETCH_POSTS`).

The binary calculates the path through the dependency graph with the maximum total latency. 
You must discover exactly how it formats its output, how it handles tie-breakers, cycles, or invalid inputs (like undeclared nodes or malformed lines), by feeding it various test inputs.

Requirements:
1. Analyze the `/app/graph_oracle` binary's I/O behavior. You may want to write a small fuzzer using property-based testing (e.g., Python's `hypothesis` library) to continuously compare your Python script's output against the legacy binary during your development.
2. Write a Python script at `/home/user/graph_eval.py` that reads from `sys.stdin` and writes to `sys.stdout`.
3. Your script must replicate the legacy binary's output byte-for-byte, including all error messages, cycle detection warnings, and the final critical path string.

The final evaluation will automatically fuzz your Python script against the `/app/graph_oracle` binary using thousands of randomly generated valid and invalid graphs to ensure 100% equivalence.