You have been given access to a C++ project repository at `/home/user/math_sim`. This project performs a high-performance parallel numerical calculation (computing the sum of squares up to 10,000,000). 

Recently, the team noticed that the program sometimes outputs incorrect results. We suspect a regression was introduced somewhere in the last 200 commits. Additionally, the project is currently failing to build due to a dependency version conflict in the build configuration, and there have been reports of the program failing to start because it cannot find its configuration file.

Your objectives are:
1. **Resolve Dependency Conflict**: Fix the `CMakeLists.txt` in the `main` branch so that the project successfully builds with the currently installed system libraries.
2. **System Call Tracing**: The executable is failing to read its configuration file, causing a startup error. Use system call tracing (e.g., `strace`) to figure out where the program is actually looking for the configuration file, and create/move the file to the expected location with the content `{"threads": 4}`.
3. **Bisect the Regression**: Use `git bisect` to identify the exact commit that introduced the mathematical correctness regression (the program should consistently output `333333383333335000000`). Save the full, 40-character commit hash of this bad commit to `/home/user/bad_commit.txt`.
4. **Fix the Bug**: The regression was caused by a concurrency issue (race condition) introduced to "optimize" the calculation. Fix the bug in the `main` branch's `src/main.cpp` so that it uses proper synchronization (e.g., `std::atomic` or `std::mutex`) and produces the correct result deterministically.
5. **Generate Final Output**: Build the fixed project and run it. Save the standard output of the successful, fixed run to `/home/user/result.txt`.

Constraints:
- Do not change the total number of iterations or the mathematical formula.
- The project must build using standard `cmake . && make`.