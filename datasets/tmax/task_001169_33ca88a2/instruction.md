You are an engineer building a custom polyglot build system from scratch. To schedule tasks optimally across different languages, you need a dependency resolver that calculates the cumulative cost of each build target and orders them correctly.

A previous engineer vendored the `toposort` Python package (version 1.10) into our build container at `/app/toposort-1.10` to help with DAG resolution, but they accidentally introduced a bug into the vendored source code while trying to patch it. 

Your tasks are:
1. Identify and fix the deliberate perturbation in the vendored `toposort` package at `/app/toposort-1.10`.
2. Write a Python script at `/home/user/scheduler.py` that parses a build manifest, computes the cumulative build cost for each target, and outputs the ordered execution plan.

The script must accept exactly one command-line argument: the path to a JSON build manifest file.
The JSON manifest has the following structure:
```json
{
  "binary_a": {"cost": 10, "deps": ["lib_b", "lib_c"]},
  "lib_b": {"cost": 5, "deps": ["lib_d"]},
  "lib_c": {"cost": 8, "deps": []},
  "lib_d": {"cost": 2, "deps": []}
}
```

The `cumulative_cost` of a target is its own `cost` plus the sum of the `cumulative_cost` of all its *immediate* dependencies.
Wait, that is recursive. Explicitly: `cumulative_cost(T) = cost(T) + sum(cumulative_cost(D) for D in deps(T))`. 

Your script `/home/user/scheduler.py` must:
1. Ensure `/app/toposort-1.10` is used for topological sorting (e.g., by adding it to `sys.path`).
2. Calculate the cumulative cost for all targets.
3. Determine a valid topological execution order (a target can only be built *after* all its dependencies are built).
4. If multiple valid topological orders are possible at any step, break ties by sorting the available targets *alphabetically* by their target name.
5. Print to `stdout` a strict JSON array of objects representing the final schedule, like so:
```json
[
  {"target": "lib_c", "cumulative_cost": 8},
  {"target": "lib_d", "cumulative_cost": 2},
  {"target": "lib_b", "cumulative_cost": 7},
  {"target": "binary_a", "cumulative_cost": 25}
]
```

Ensure your script only prints this JSON array to standard output. Do not print additional logs to standard output.