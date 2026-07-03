I am working on a custom Python-based build system to compile a multi-file project. Currently, the project fails to compile because the build script generates an incorrect linking order. 

The script, located at `/home/user/project/resolver.py`, is supposed to parse a dependency graph from `/home/user/project/deps.json` and determine the correct compilation sequence (a module can only be compiled after all its dependencies are compiled). Unfortunately, the graph traversal logic is flawed and outputs an invalid order.

Additionally, we need to benchmark the compilation process by calculating the "critical path" cost. Each module has a compilation time cost specified in `/home/user/project/costs.json`. The critical path is the maximum total time required to build a root module, tracing the cost from the deepest dependency up to the root.

Your task:
1. Fix the dependency resolution logic in `/home/user/project/resolver.py` so that it correctly performs a topological sort.
2. Modify the script so that when executed, it writes the correct build order as a comma-separated list of module names to `/home/user/build_order.txt`. Any valid topological sort is acceptable.
3. Implement the critical path calculation (a numerical algorithm computing the maximum path weight in the DAG) in the script. The script must write the integer value of the critical path cost to `/home/user/critical_path.txt`.
4. Run your script to generate the output files.

All required files (`deps.json`, `costs.json`, and the template `resolver.py`) are located in `/home/user/project`. You must use Python to implement the logic.