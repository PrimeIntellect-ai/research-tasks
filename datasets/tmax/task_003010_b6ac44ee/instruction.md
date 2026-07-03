You are a build engineer managing a Bash-based artifact pipeline. A recent CI pipeline is failing. The project concatenates multiple bash modules into a single executable, but the current build script is combining them in the wrong order, missing a critical security patch, and the resulting artifact suffers from a resource leak that exhausts disk inodes in a cache directory during CI fuzz testing.

Your tasks are to fix the pipeline, patch the code, resolve the leak, and write a test script to verify robustness.

Setup Details:
The project is located at `/home/user/build_project`.
Inside, you will find:
- `src/utils.sh`
- `src/core.sh`
- `src/main.sh`
- `update.patch`
- `build.sh`
- `cache/` (a directory for temporary files)

Instructions:
1. **Apply the Patch**: Apply `update.patch` to `src/core.sh`.
2. **Fix the Build System**: The current `build.sh` blindly concatenates files using `cat src/*.sh > dist/app.sh`, which uses alphabetical order (`core.sh` -> `main.sh` -> `utils.sh`). This breaks dependency rules. Modify `build.sh` so that it concatenates the files into `dist/app.sh` in this exact logical order:
   - `src/utils.sh`
   - `src/core.sh`
   - `src/main.sh`
   Make sure `build.sh` also makes `dist/app.sh` executable.
3. **Fix the Resource Leak**: Run `build.sh`. The resulting `dist/app.sh` takes an integer argument. Whenever it runs, it creates a temporary file in `/home/user/build_project/cache/`. It fails to clean up this file before exiting. Modify `src/main.sh` (and rebuild) to ensure that the cache file is deleted right before the script exits successfully.
4. **Property-based Testing**: Write a bash script at `/home/user/build_project/fuzz.sh`. This script must:
   - Run `dist/app.sh` 50 times in a loop.
   - For each run, pass a different random integer (using Bash's `$RANDOM`) as the argument.
   - After each run, verify that the exit code is 0 AND that the `/home/user/build_project/cache/` directory is completely empty.
   - If any run fails or leaves a file behind, `fuzz.sh` should exit with code 1 immediately.
   - If all 50 runs succeed and the cache remains clean, write the exact string "FUZZING SUCCESS" to `/home/user/build_project/report.txt` and exit with code 0.

Ensure your `fuzz.sh` works correctly and that `/home/user/build_project/report.txt` is generated at the end of your process.