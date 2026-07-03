You are a web developer working on a backend API server that features a high-performance, dynamic plugin system. The plugins have complex load-order constraints defined by dependencies. 

Your team uses a legacy C library, `libdeps.c`, to parse these dependency rules from a text file, but it crashes on large configurations due to a memory safety issue (undefined behavior/segfaults). 

You need to write the Rust orchestration code to interact with this C library, resolve the dependencies, and output the exact order the plugins should be loaded.

Here is your objective:
1. Navigate to `/home/user/plugin_manager`.
2. Fix the memory allocation bug in `/home/user/plugin_manager/src/libdeps.c`. The file parses a list of dependencies where each line `A B` means "Plugin A depends on Plugin B" (so B must be loaded before A).
3. Complete the Rust application in `/home/user/plugin_manager/src/main.rs`. 
   - It already contains the FFI bindings to call `parse_deps`.
   - You must design a custom graph data structure in Rust to represent the dependencies.
   - Implement a constraint satisfaction algorithm (Topological Sort) to determine the correct load order for the plugins. 
   - **Crucial Tie-breaking Rule**: If multiple plugins have all their dependencies met and can be loaded at the same time, *always pick the plugin with the smallest numerical ID first*.
4. Execute your Rust program so that it writes the final load order of plugin IDs as a single space-separated string to `/home/user/load_order.txt`.

Example: If the file `/home/user/load_order.txt` requires plugins 3, 2, and 1 in that order, its contents should be exactly `3 2 1`.

Ensure your Rust code compiles cleanly and outputs the solution file directly.