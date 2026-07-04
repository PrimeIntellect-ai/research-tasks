You are a web developer working on a backend feature that requires processing data through a custom C pipeline loaded into Python. The pipeline consists of four shared libraries: `libA`, `libB`, `libC`, and `libD`. 

The development team has dumped several compiled versions of these libraries into `/home/user/libpool/`. Because they were compiled without strict linkage (no `-l` flags), they have unresolved undefined symbols. 

Your task is to write a Bash script `/home/user/resolve.sh` that performs the following:
1. Analyzes the shared objects in `/home/user/libpool/` to resolve the symbol dependency graph (you can use tools like `nm` or `readelf`). `libA.so` is the entry point loaded by Python.
2. Selects exactly one version of each library (`libA`, `libB`, `libC`, `libD`) such that all undefined symbols originating from `libA`'s execution path are satisfied by the chosen libraries.
3. Constraint: The final combination must pass the end-to-end test `/home/user/e2e_test.py`.
4. Creates symlinks in `/home/user/active_libs/` named `libA.so`, `libB.so`, `libC.so`, and `libD.so` pointing to your chosen versions.
5. Runs the end-to-end test with the appropriate `LD_LIBRARY_PATH`.
6. Writes the basenames of the 4 chosen library files (e.g., `libA_vX.so`) to `/home/user/solution.log`, one per line, sorted alphabetically.

Ensure your bash script creates the `active_libs` directory if it does not exist, clears it, sets up the symlinks, and executes the python test successfully.

To complete the task, execute your `/home/user/resolve.sh` script so that `/home/user/solution.log` is generated and `/home/user/e2e_test.py` completes without errors.