You are a developer tasked with debugging a failing build in a C project. 

The project, located at `/home/user/trajectory_calc`, calculates projectile trajectories. Recently, a regression was introduced that causes the test suite build to fail. The repository uses Git.

Your objectives are:
1. **Find the regression:** Use `git bisect` to identify the exact commit hash that introduced the build failure. The `v1.0` tag is known to be good, and `HEAD` is bad. Write the full 40-character commit hash of the *first bad commit* to `/home/user/bad_commit.txt`.
2. **Diagnose and Fix:** The build fails because a developer incorrectly altered the physics formula in `trajectory.c`. Identify the compilation error, diagnose the intent, and correct the formula in `trajectory.c`. The correct formula for the Y-axis position is standard projectile motion under gravity (using `g = 9.8`): `y = v0_y * t - 0.5 * g * t^2`. Make sure the code compiles cleanly by running `make`.
3. **Fuzz Testing:** To ensure the function handles unexpected values gracefully without crashing, write a LLVM libFuzzer target in a new file `/home/user/trajectory_calc/fuzz_test.c`. The fuzzer should consume a `double` for `v0_y` and a `double` for `t`, and call the `calc_y` function. 
4. Compile your fuzzer executable to `/home/user/trajectory_calc/fuzzer` using clang with `-fsanitize=fuzzer`.

**System State After Completion:**
- `/home/user/bad_commit.txt` contains only the bad commit hash.
- `/home/user/trajectory_calc/trajectory.c` contains the corrected implementation.
- `/home/user/trajectory_calc/fuzzer` is a compiled libFuzzer executable.
- The project successfully builds using `make`.