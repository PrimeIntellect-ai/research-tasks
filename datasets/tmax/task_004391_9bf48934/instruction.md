You are an engineer tasked with porting a legacy data processing tool to run in a minimal Linux container environment. We have a shared C library and a C++ main application, but they are failing to build and run together due to ABI mismatch and build orchestration issues.

Your objectives:
1. Examine `/home/user/processor.cpp` and `/home/user/libmathops.c`. The C++ application is supposed to call the `compute_mean` function from the C shared library, but it currently fails to link because of ABI name mangling issues. Fix `processor.cpp` so it correctly links to the C library.
2. In `/home/user/processor.cpp`, implement the missing logic to:
   - Parse the structured CSV file at `/home/user/data.csv`. The file has headers `id,value`.
   - Extract the `value` column (as `double`).
   - For every consecutive, overlapping window of size 3 (e.g., elements 0,1,2, then 1,2,3), call `compute_mean` from the shared library to calculate the moving average.
   - Sort the resulting moving averages in **descending** order.
   - Write the sorted averages to `/home/user/output.txt`, with exactly one number per line, formatted to 2 decimal places.
3. The minimal container does not have Make or CMake. Write a build script `/home/user/build.sh` that:
   - Compiles `libmathops.c` into a shared library `libmathops.so`.
   - Compiles `processor.cpp` into an executable named `processor`, dynamically linking it to `libmathops.so`. Ensure the runtime linker can find the shared library in the current directory (e.g., using rpath).
4. Run your build script and execute `./processor` to generate `/home/user/output.txt`.

The initial files (`data.csv`, `processor.cpp`, `libmathops.c`) will be present in `/home/user/`.