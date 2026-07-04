You are helping a developer organize their project files and build pipeline. The developer has a C library designed to read a dependency file, perform a topological sort (graph dependency resolution), and return the correct build order. They intend to call this C library from a Python script to automate the organization of their workspace.

However, the C library is crashing with segmentation faults due to memory safety issues (Undefined Behavior). 

Here is what you need to do:

1. Look at the C source file located at `/home/user/workspace/graph.c`. It contains the function `char** get_build_order(const char* filepath, int* out_count);`. 
2. Fix the memory safety bugs in `/home/user/workspace/graph.c`. There are at least two distinct memory-related bugs (one involving string allocation bounds, and another involving the lifetime/scope of the returned array). Ensure the topological sorting logic remains intact.
3. Compile the fixed C code into a shared library named `/home/user/workspace/libgraph.so`.
4. Write a Python script at `/home/user/workspace/resolve.py`. This script must:
   - Load `libgraph.so` using the `ctypes` module.
   - Define the correct argument and return types for the FFI boundary to `get_build_order`.
   - Call `get_build_order` passing the path to the provided dependency file (`/home/user/workspace/deps.txt`).
   - Iterate through the returned C string array to get the module names in the correct build order.
   - Write these module names, in order, one per line, to a new file at `/home/user/workspace/build_order.txt`.
   - Properly call the provided `free_build_order(char** order, int count)` C function from Python to prevent memory leaks before exiting.

The dependency file `/home/user/workspace/deps.txt` uses the format `target: dep1 dep2 ...` per line.

Ensure the final `build_order.txt` is created with the correctly ordered modules. If there are multiple valid topological sorts, the logic in `graph.c` is deterministic and will produce one specific valid output—do not alter the sorting algorithm itself, only fix the memory safety issues.