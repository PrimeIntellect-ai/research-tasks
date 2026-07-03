You are an engineer tasked with fixing a custom build system that is currently failing due to a circular dependency in a C++ project. 

The project's dependency graph is defined in a custom text format in the file `/home/user/project/build.deps`. 

The format of this file is as follows:
- Each line defines a module and its dependencies.
- Syntax: `ModuleName -> Dep1, Dep2, Dep3`
- Lines can have arbitrary whitespace. Empty lines are ignored.

Your task has four parts:

1. **Parser and Graph Traversal (C++)**:
Write a C++ program at `/home/user/project/cycle_detector.cpp` that:
- Reads the `build.deps` file.
- Uses a custom state-machine based parser (do not use external regex libraries) to parse the module names and their dependencies.
- Builds a directed graph in memory.
- Uses graph traversal (e.g., Depth First Search) to detect any circular dependency.
- If a cycle is found, it must write the cycle to `/home/user/project/cycle.log` in the exact format: `Cycle: NodeA -> NodeB -> NodeC -> NodeA`. 
  *Constraint:* To ensure determinism, if a cycle exists, report the sequence starting with the module whose name is lexicographically smallest.
- The C++ program should return an exit code of `1` if a cycle is detected, and `0` if the graph is a valid Directed Acyclic Graph (DAG).

2. **Execute and Log**:
Compile your C++ program and run it against the broken `/home/user/project/build.deps` file to generate `/home/user/project/cycle.log`.

3. **Fix the Project**:
Fix the circular dependency in `/home/user/project/build.deps`. To do this, locate the dependency edge from `Utils` to `Network` that is causing the cycle and remove `Network` from the `Utils` dependency list. If `Utils` has no other dependencies, you may leave it as `Utils ->` or remove the line entirely.

4. **CI Pipeline Setup**:
Create a bash script at `/home/user/project/ci_pipeline.sh` that acts as a CI/CD check. The script must:
- Be executable.
- Compile `/home/user/project/cycle_detector.cpp` to `/home/user/project/detector`.
- Run `/home/user/project/detector /home/user/project/build.deps`.
- Exit with `0` if the build graph is valid, or fail with `1` if a cycle is found.

Ensure all file paths are exact and the final state leaves a fixed `build.deps`, a correct `cycle.log` from the broken state, and a working `ci_pipeline.sh`.