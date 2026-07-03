You are acting as a QA Engineer setting up a continuous testing environment for a new C-based web security tool called `log_sanitizer`. Your goal is to fix the current broken build, perform a database schema migration, implement a basic property-based fuzzing script, and tie it all together in a CI pipeline script.

The project is located in `/home/user/project/`.

Here are your tasks:

1. **Fix the C Code and Makefile**:
   - The source code is at `/home/user/project/sanitizer.c` and the build script is `/home/user/project/Makefile`.
   - The `Makefile` has a `build` target, but it is currently failing because the C code has missing header includes and a strict compiler flag (`-Werror`) is catching implicit function declarations.
   - Fix `sanitizer.c` so it compiles successfully using the existing `Makefile` (do not remove `-Werror` from the Makefile). The compiled output should be an executable named `sanitizer` in the same directory.
   - The `sanitizer` program takes a single string argument and replaces any `<` or `>` characters with `_`, printing the result to standard output.

2. **Schema Migration**:
   - There is an SQLite database used for testing at `/home/user/logs.db`. It currently contains a table named `access_logs` with columns `id INTEGER PRIMARY KEY` and `payload TEXT`.
   - Write a bash script at `/home/user/project/migrate.sh` that safely alters this table to add a new column: `threat_level INTEGER DEFAULT 0`.
   - Make sure `migrate.sh` is executable.

3. **Property-Based Testing (Fuzzer)**:
   - Write a bash script at `/home/user/project/fuzz.sh` (make it executable) that tests the `sanitizer` executable.
   - The script should generate 50 random alphanumeric strings (lengths between 10 and 20 characters). You can use `/dev/urandom` or `$RANDOM` for this.
   - For each string, inject a random `<` or `>` character into it, pass it to `./sanitizer`, and verify the property: **the output must not contain any `<` or `>` characters.**
   - If the property holds for all 50 inputs, append the line `FUZZING_PASSED` to `/home/user/project/test_results.txt` and exit with code 0. If it fails, append `FUZZING_FAILED` and exit with code 1.

4. **CI/CD Pipeline Setup**:
   - Create a shell script at `/home/user/project/ci_pipeline.sh` (make it executable) that orchestrates the above steps in order:
     a) Run `make clean` then `make build`
     b) Run `./migrate.sh`
     c) Run `./fuzz.sh`
   - If any command fails, the script must immediately exit with a non-zero exit code.
   - If all commands succeed, the script must create an empty file at `/home/user/project/ci_success` and exit with code 0.

Once you have completed these steps, manually run `/home/user/project/ci_pipeline.sh` to ensure everything works and the `ci_success` file is generated.