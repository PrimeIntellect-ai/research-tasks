You are a developer organizing a massive set of legacy project files and their dependency graphs. We use an old proprietary tool to analyze these dependencies, located at `/app/legacy_analyzer/analyze_deps` (it is a stripped, packed binary). 

Unfortunately, this legacy binary is highly unstable. It frequently crashes with segmentation faults (due to memory safety issues and undefined behavior) when it encounters malformed dependency graphs, specifically:
1. Circular dependencies (cycles in the graph).
2. Malformed file paths containing directory traversal attacks (`../` or `..\\`) or invalid UTF-8 sequences.

Your task is to write a C++ sanitiser tool that acts as a gatekeeper before we pass files to the legacy analyzer. 

Requirements:
1. Create a C++ program at `/home/user/project/sanitise_deps.cpp`.
2. The program must accept a single command-line argument: the path to a dependency file.
    - Example invocation: `./sanitise_deps /path/to/dep_file.txt`
3. The dependency file format consists of lines defining a target and its dependencies, separated by spaces.
    - Format: `target dependency1 dependency2 ...`
    - Empty lines should be ignored.
4. Your program must parse the graph and perform the following checks:
    - **Encoding/Path Safety:** Every target and dependency string must be valid UTF-8. They must NOT contain null bytes (`\0`), and must NOT contain directory traversal sequences (i.e., the exact substrings `../` or `..\`).
    - **Graph Traversal:** The dependency graph must NOT contain any cycles (e.g., A depends on B, B depends on A).
5. Output exactly `ACCEPT` to standard output (with a newline) and exit with code 0 if the file is completely valid.
6. Output exactly `REJECT` to standard output (with a newline) and exit with code 1 if the file violates any of the rules above.
7. Write a `Makefile` in `/home/user/project` that compiles `sanitise_deps.cpp` into an executable named `sanitise_deps` using `g++` with `-O2` and `-std=c++17`.

Ensure your C++ code is memory safe and robust against maliciously malformed input files.