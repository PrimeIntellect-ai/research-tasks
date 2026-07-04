You are a platform engineer responsible for maintaining CI/CD pipelines and core infrastructure libraries. A new requirement mandates a constraint satisfaction solver written in C++ to be used by an existing C-based scheduling application.

Your task is to implement the solver, manage the C/C++ ABI boundary, orchestrate the build system, and produce the final executable.

1. **Implement the Solver:**
Create a file `/home/user/solver.cpp` containing a C++ implementation of a Constraint Satisfaction Problem (CSP) solver.
The solver must expose the following C ABI compatible function:
`extern "C" int solve_csp(int num_tasks, int num_workers, const int* conflicts, int num_conflicts, int* out_assignments);`

- `num_tasks`: The number of tasks (indexed `0` to `num_tasks - 1`).
- `num_workers`: The number of available workers (indexed `0` to `num_workers - 1`).
- `conflicts`: A flat array of size `num_conflicts * 2` representing pairs of tasks that *cannot* be assigned to the same worker. For example, `conflicts[2*i]` and `conflicts[2*i+1]` are mutually exclusive for any worker.
- `out_assignments`: An array of size `num_tasks` allocated by the caller. If a valid assignment is found, populate this array where `out_assignments[i]` is the worker ID assigned to task `i`.

The function must return `1` if a valid assignment exists, and `0` otherwise. You must design and use a custom C++ graph/adjacency data structure to represent the constraints and implement a backtracking search to find a valid assignment.

2. **Polyglot Build Orchestration:**
A C application `/home/user/app.c` is already provided. It calls your `solve_csp` function to test various scheduling constraints.
Create a `/home/user/Makefile` that:
- Compiles `solver.cpp` into a shared library named `libsolver.so`.
- Compiles `app.c` and links it against `libsolver.so` to produce an executable named `app`.
- Ensures that the `app` executable dynamically loads `libsolver.so` at runtime *without* requiring `LD_LIBRARY_PATH` to be set (you must use the rpath linker flag pointing to the current directory).

3. **Execution:**
Run `make` to build the project, then run `./app`. The C application will automatically verify your solver's assignments and write the validation results to `/home/user/output.txt`.

Ensure all files are created in `/home/user`.