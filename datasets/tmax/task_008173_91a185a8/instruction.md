I am migrating our legacy data processing pipeline from Python 2 to Python 3. Unfortunately, during the migration, conflicting dependency issues (similar to npm peer dependency hell) made our Python-based test runner completely unusable. To keep development moving, I decided to rewrite the test automation and shared library management completely in Bash.

I need you to write a Bash script at `/home/user/build_and_test.sh` that performs the following steps to build, link, and test our custom C serialization library:

1. Create the directories `/home/user/lib/` and `/home/user/bin/` if they do not already exist.
2. Compile the C source file `/home/user/src/data_processor.c` into a shared library named `libdataproc.so`, placing it in `/home/user/lib/`. Ensure it is compiled correctly as a shared object (position-independent code).
3. Compile the unit test file `/home/user/src/test_runner.c` into an executable named `/home/user/bin/test_runner`. It must link against the `libdataproc.so` shared library you just built.
4. Execute `/home/user/bin/test_runner`, passing the binary file `/home/user/data/input.dat` as its first argument. The executable deserializes the binary data and outputs a JSON payload. (Note: Ensure the shared library can be located at runtime).
5. Capture the standard output of the test runner and save it exactly to `/home/user/test_results.json`.
6. Check the exit status of the test runner. If it succeeds (exits with 0), write the exact string `PASS` to `/home/user/status.log`. If it fails, write `FAIL` to `/home/user/status.log`.

Make sure your script has execute permissions, but do not execute it for me—I will execute `/home/user/build_and_test.sh` myself after you create it.