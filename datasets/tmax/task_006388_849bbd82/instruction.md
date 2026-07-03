You are helping a developer migrate their legacy custom build system from Python 2 to Python 3. The build system reads a JSON dependency graph to generate a Makefile for a small C project, but it currently has several issues preventing the project from building correctly.

The project is located in `/home/user/project/`.
Inside this directory, you will find:
- `build_system.py`: The legacy Python 2 script that generates the Makefile.
- `deps.json`: A JSON file defining the module dependency graph.
- `src/`: A directory containing the C source files (`main.c`, `math_ops.c`, `string_ops.c`, `advanced_math.c`).

Your objective is to fix the build system, generate the Makefile, compile the C code, and produce a final output log.

Specifically, you need to perform the following steps:

1. **Migrate to Python 3:** Update `/home/user/project/build_system.py` so it runs flawlessly under Python 3. Fix any Python 2 specific syntax (like `print` statements or dictionary methods).
2. **Fix Dependency Resolution:** The `get_all_dependencies(graph, root)` function in `build_system.py` contains a logical bug. It currently only resolves immediate, first-level dependencies. You must rewrite this function to perform a full graph traversal (e.g., using DFS or BFS) so that it returns ALL transitive dependencies for a given root.
3. **Fix the Linking Error:** The generated Makefile fails to link because `advanced_math.c` uses functions from the math library (`<math.h>`). Modify `build_system.py` so that if `advanced_math` is in the resolved dependency list, the generated linking command in the Makefile appends `-lm` to the end of the `gcc` linking command.
4. **Implement Conditional Cross-Compilation:** Modify `build_system.py` so that it checks for an environment variable named `TARGET_ARCH`. If `TARGET_ARCH` is set to `arm`, the script must add `-DARM_MODE=1` to the `CFLAGS` variable in the generated Makefile.
5. **Generate and Build:** 
   - Run the updated Python script: `python3 build_system.py` to generate the `Makefile`.
   - Compile the project by running `make` with the environment variable `TARGET_ARCH=arm`.
   - This should successfully compile an executable located at `/home/user/project/bin/app`.
6. **Execution:** Run the compiled executable `./bin/app` and redirect its standard output to `/home/user/project/result.txt`.

Do not modify the C source files or the `deps.json` file. Only modify `build_system.py` and run the necessary commands to complete the process.