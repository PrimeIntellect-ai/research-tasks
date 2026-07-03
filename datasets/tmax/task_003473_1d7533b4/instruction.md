You are a systems programmer debugging a C library linking issue. A complex numerical application is failing to compile because its dynamic libraries are being linked in the wrong order. 

In C linking, if Library A depends on Library B, Library A must appear *before* Library B in the linking command. Furthermore, to satisfy the build system's deterministic output constraints, any ties in the linking order must be resolved using a mathematical "weight" assigned to each library: the library with the *highest* weight must be linked first when multiple libraries are eligible.

You have been provided with the dependency graph in JSON format at `/home/user/deps.json`. 

The structure of the JSON file is a dictionary where each key is a library name, and its value is an object containing:
- `deps`: a list of library names that this library depends on.
- `weight`: an integer weight used for tie-breaking.

Your task is to write a Bash script, `/home/user/solve_linking.sh`, that calculates the correct topological linking order. The script should read `/home/user/deps.json` and output the correct order to `/home/user/link_order.txt` (one library name per line).

Rules for the ordering:
1. It must be a valid topological sort (if A depends on B, A must appear before B).
2. At any step, if there are multiple libraries with an in-degree of 0 (i.e., all the libraries that depend on them have already been placed in the sequence), you must choose the library with the highest `weight`.
3. You may use `jq` and any standard Bash utilities.
4. Execute your script so that `/home/user/link_order.txt` is populated with the final answer.