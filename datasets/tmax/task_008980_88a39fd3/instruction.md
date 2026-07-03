You are helping me migrate a legacy data processing pipeline. Our infrastructure is moving from Python 2 to Python 3, and I'm currently stuck trying to get the pipeline's C extensions and Python parser working together again. 

The project is located in `/home/user/data_migration`. It processes a Directed Acyclic Graph (DAG) of data nodes, transforming values using a custom C program.

Here is what you need to do:

1. **Fix the C build system**: There is a CMake project in `/home/user/data_migration/c_src`. It builds a shared library (`libmathops.so`) and an executable (`calc_node`). Currently, `make` fails because `calc_node` cannot find the `mathops` library at link time. Fix `CMakeLists.txt` so it compiles successfully. Ensure that the built executable runs without `LD_LIBRARY_PATH` errors (e.g., CMake's RPATH should work out of the box once properly linked).

2. **Migrate the Python parser**: There is a Python script `/home/user/data_migration/dag_parser.py`. It reads a custom `.node` file and extracts its metadata. It is currently written in Python 2. Upgrade it so it runs under Python 3 without syntax or runtime errors. Do not change its command-line interface.

3. **Write the Pipeline Orchestrator in Bash**:
Create a Bash script at `/home/user/data_migration/process_graph.sh`. This script will orchestrate the data processing.
- The script should take exactly one argument: the path to a starting `.node` file (e.g., `/home/user/data_migration/nodes/A.node`).
- It must parse the graph dependencies by looking at the output of `python3 dag_parser.py <node_file>`. The output contains a list of dependency filenames and a numerical value.
- Implement a graph traversal in Bash to process the nodes in **post-order** (process a node's dependencies before processing the node itself). If a node has multiple dependencies, process them in the order they appear in the parser's output. Ensure no node is processed more than once.
- For each processed node:
  - Extract its `VALUE` using the Python parser.
  - Pass this `VALUE` to the compiled `./c_src/build/calc_node` executable as a command-line argument. The executable will print a transformed integer.
  - Maintain a running accumulator in your Bash script (initialized to 0). For each node processed, update the accumulator using the formula: `accumulator = (accumulator * 3 + transformed_integer) % 100000`.

4. **Output format**:
Your Bash script (`process_graph.sh`) must write its results to `/home/user/data_migration/result.txt`.
For every node processed, append a line: `Processed: <NodeName>` (where NodeName is the basename of the `.node` file without the extension).
After processing all nodes, append a final line: `Final Accumulator: <FinalValue>`.

Ensure your Bash script is executable and robust. Run it on `/home/user/data_migration/nodes/root.node` as a final test.