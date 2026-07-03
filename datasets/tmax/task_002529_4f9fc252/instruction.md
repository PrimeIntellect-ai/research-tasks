You are a systems programmer working on a hybrid Python/C project located in `/home/user/project`. 

The project consists of a Python script (`wrapper.py`) that uses a C shared library (`libsolver_core.so`) via `ctypes`. The C library relies on another shared library (`libmath_utils.so`). 

Currently, the project is completely broken. Here is what you need to do:

1. **Fix the CMake Linking Issue:**
   The `CMakeLists.txt` is incomplete. When you build the project and try to run `wrapper.py`, Python throws an `OSError` about undefined symbols or missing libraries. Fix the `CMakeLists.txt` so that `solver_core` properly links against `math_utils` and the Python script can load the library successfully without needing to manually set `LD_LIBRARY_PATH` (e.g., configure the RPATH correctly in CMake, or ensure the library is found relative to the build directory). 
   Build the project in `/home/user/project/build`.

2. **Fix C Memory Safety Issues:**
   The C library `src/solver_core.c` has a function `int compute_score(int* items, int num_items)`. It contains memory safety issues (undefined behavior/buffer overflow) and a memory leak. Use memory debugging tools (like `valgrind`) to identify and fix these issues so that the function is completely memory safe and leak-free.

3. **Solve the Constraint Satisfaction Problem in Python:**
   Open `/home/user/project/wrapper.py`. You need to write a Python algorithm to solve a Graph Coloring constraint satisfaction problem. 
   Find a valid assignment of colors (represented by integers 1, 2, and 3) to 5 nodes (numbered 0 to 4) such that no two adjacent nodes have the same color.
   The undirected edges of the graph are: (0,1), (1,2), (2,3), (3,4), (4,0), and (0,2).
   Node 0 MUST be assigned color 1.
   
4. **Integration:**
   In `wrapper.py`, once the valid coloring array is found (e.g., `[color0, color1, color2, color3, color4]`), pass this integer array and its length (5) to the `compute_score` function in the compiled `libsolver_core.so` using `ctypes`.
   Write the integer result returned by the C function to a file exactly at `/home/user/result.txt`.

Ensure your Python script works cleanly and `/home/user/result.txt` contains only the final integer score.