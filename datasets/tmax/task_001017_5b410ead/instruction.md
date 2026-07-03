I am a web developer building a video ad-placement feature for our streaming platform. We need to determine if an exact "ad pod" duration (a specific number of seconds) can be perfectly filled by a subset of our available ad creatives. This is a classic constraint satisfaction problem (Subset Sum).

To ensure high performance, our backend relies on a C extension. However, the current C implementation (`/home/user/solver/solver.c`) has a memory safety bug (undefined behavior/segmentation fault) that crashes the process for certain inputs. Furthermore, the provided `Makefile` in `/home/user/solver/` is broken and fails to properly compile the C code into a shared object library (`libsolver.so`).

Your task is to:
1. Fix the `Makefile` so that running `make` correctly compiles `solver.c` into a dynamic shared library named `libsolver.so` (ensure proper compiler flags for shared libraries are used).
2. Fix the memory safety issue (undefined behavior/buffer overflow) in `solver.c`. The function signature `int subset_sum(int* arr, int n, int target)` must remain exactly the same.
3. Write a Python script at `/home/user/solve_api.py` that loads `libsolver.so` using the `ctypes` module.
4. Using your Python script, invoke the C function to test if the following ad pod target durations can be perfectly filled using the available ad lengths: `[15, 30, 45, 60, 90, 120]`. 
   The target durations to check are: `105`, `110`, `135`, `140`, `210`, and `250`.
5. Your Python script must save the results to a JSON file at `/home/user/results.json`. The JSON file should be a dictionary mapping the target duration (as a string) to a boolean value representing whether it can be filled.

Example of expected JSON format:
```json
{
  "105": true,
  "110": false,
  "135": true,
  "140": false,
  "210": true,
  "250": false
}
```

Please make the necessary fixes, write the Python integration, and generate the final `results.json` log file.