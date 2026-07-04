You are helping a developer organize a messy repository of project files by determining their build dependency order.

You have a workspace at `/home/user/project_workspace`. Inside, there are two main directories:
1. `/home/user/project_workspace/source_files`: Contains a set of `.c` and `.h` files with various `#include "..."` directives.
2. `/home/user/project_workspace/extractor`: A Rust project intended to parse these files and extract their dependencies.

However, the pipeline is currently broken.

Your task consists of three phases:

**Phase 1: Fix the Rust Extractor**
The Rust tool in `/home/user/project_workspace/extractor` is designed to read all files in the `source_files` directory and output their dependencies. Unfortunately, the original developer left a borrow-checker/lifetime bug in `/home/user/project_workspace/extractor/src/main.rs`.
Fix the compilation error so that `cargo run` works successfully. When run, it reads the `source_files` directory and writes the dependencies to `/home/user/project_workspace/deps.hex`. 
The format of `deps.hex` is a continuous hex-encoded string representing lines of dependency pairs: `<dependent_file> <dependency_file>\n`.

**Phase 2: Write the C Analyzer**
Write a C program at `/home/user/project_workspace/analyzer.c`.
This program must:
1. Read the hex-encoded file `/home/user/project_workspace/deps.hex`.
2. Decode the hex data back into ASCII text (character/data decoding).
3. Parse the dependency pairs.
4. Perform a topological sort (graph traversal and dependency resolution) to determine the correct build order of all unique files mentioned in the dependencies.
*Constraint:* When multiple files have no pending dependencies and can be processed, break ties by selecting the file that comes first alphabetically.

**Phase 3: Generate the Output**
Your C program must compile to `/home/user/project_workspace/analyzer` and, when executed, it must output the ordered list of files, one per line, to `/home/user/project_workspace/build_order.txt`.

*Note:* You are restricted to standard CLI tools, Bash built-ins, and standard C/Rust libraries. Do not install external libraries (no external crates for the Rust project except what is already there, no third-party C libraries).