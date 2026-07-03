You are a performance engineer stepping into a newly acquired project. The project is a C-based performance profiling library located at `/home/user/fast_profiler`. 

Currently, the build is failing. Additionally, the team needs to recover a lost API token for the telemetry server that was accidentally hardcoded in an older commit and then removed, and write a regression test to ensure the telemetry module behaves correctly.

Your tasks are:

1. **Build Failure Diagnosis**: Diagnose and fix the build error in the repository so that running `make all` completes successfully. Do not change the compiler flags in the `Makefile` to bypass the error.
2. **Git History Forensics**: Search the `git` history of the repository to find the old hardcoded telemetry token. Extract just the token string (e.g., `ABC-123`) and save it to a new file exactly at `/home/user/secret_token.txt`.
3. **Regression Test Construction**: 
   - Create a C regression test file at `/home/user/fast_profiler/tests/test_telemetry.c`.
   - The test should include `telemetry.h`.
   - It must programmatically set the environment variable `TELEMETRY_TOKEN` to the recovered token value (using `setenv`).
   - It should then call `telemetry_init()`.
   - The test program should return `0` if `telemetry_init()` succeeds (returns `0`), and `1` otherwise.
4. **Makefile Update**: Update the existing `/home/user/fast_profiler/Makefile` to add a `test` target.
   - The `test` target must compile `tests/test_telemetry.c` linking against the built `libtelemetry.a` to produce an executable.
   - It must run the executable.
   - If the executable exits successfully (code `0`), the `test` target must write the exact string `ALL TESTS PASSED` to `/home/user/test_result.log`.

Ensure all files are created with the exact paths and formats specified. Do not remove any existing flags from the `Makefile`.