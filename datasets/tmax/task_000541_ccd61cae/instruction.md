You are a platform engineer maintaining the CI/CD pipelines for your organization. You have a legacy pipeline configuration parser written in Python that reads custom `.pipeline` DSL files, constructs an execution graph, and determines the execution order. However, the Python script uses a highly inefficient state machine, suffers from severe memory leaks, and completely hangs when a pipeline configuration contains a circular dependency (which prevents the build).

Your task is to rewrite this tool in **Rust** to ensure memory safety, correct cycle detection, and high performance.

Here are your specific objectives:

1. **Code Translation & Parsing:**
   Analyze the legacy Python script at `/home/user/legacy_parser.py`. Translate its core parsing logic into a robust Rust state machine. 
   The DSL syntax is:
   ```
   job <name>:
     requires: [<dependency1>, <dependency2>]
   ```
   Dependencies are comma-separated. The `requires:` line may be empty: `requires: []`.

2. **Cycle Detection & Topological Sort:**
   Your Rust program must parse the file into a directed graph and determine the execution order using topological sorting.
   - If there are no cycles, output: `RESULT: SUCCESS\nORDER: <comma-separated job list>` (tie-break alphabetically if multiple jobs have no pending dependencies).
   - If a circular dependency exists, detect it and output: `RESULT: ERROR\nCYCLE: <cycle path>` (e.g., `CYCLE: A -> B -> C -> A`). Format the cycle so it starts with the alphabetically smallest node in the cycle.

3. **Memory Profiling:**
   To prove the memory leak is resolved, your Rust program must track its own heap memory usage. Implement a custom `GlobalAlloc` wrapper (wrapping `std::alloc::System`) that tracks the peak allocated bytes using an `AtomicUsize`.
   Before exiting, your program must print: `PEAK_MEM: <bytes>` to standard output.

4. **Test Fixtures & Mocks:**
   Within your Rust project, write an integration test module that uses mock filesystem setups (or in-memory string parsing fixtures) to test both a valid DAG and a circular DAG.

5. **Deployment:**
   Create a standard Rust binary crate at `/home/user/pipeline-parser`. 
   Compile it in release mode. We will execute `/home/user/pipeline-parser/target/release/pipeline_parser <file_path>` for automated testing.

Two test files exist for you to verify your implementation: `/home/user/pipelines/valid.pipeline` and `/home/user/pipelines/circular.pipeline`. Ensure your tool processes them correctly and prints the exact expected formats to `stdout`.