You are an open-source maintainer reviewing a pull request for a project that calculates and verifies CRC32 checksums of files. The PR is broken and lacks tests. Your job is to fix the build system and implement a test fixture to verify the core functionality.

The project is located in `/home/user/pr_review/`. It consists of:
- `checksum.c`: A library implementation for calculating CRC32.
- `main.c`: The main CLI tool that verifies a file's checksum.
- `Makefile`: The build script (which is currently broken).

Here are your tasks:

1. **Repair the Makefile**: 
   The `Makefile` is supposed to compile `checksum.c` into a shared library `libchecksum.so`, and then compile `main.c` into an executable named `verifier` linked against `libchecksum.so`. 
   Currently, the `Makefile` fails to link the shared library properly, and even if it did, running `./verifier` would fail at runtime because it cannot find the shared library.
   Fix the `Makefile` so that:
   - Running `make` successfully builds both `libchecksum.so` and `verifier`.
   - The `verifier` executable can find `libchecksum.so` at runtime *without* needing to modify environment variables like `LD_LIBRARY_PATH`. You must configure the executable's RPATH to look in its origin directory.

2. **Create a Test Fixture**:
   Write a Python script at `/home/user/pr_review/test_fixture.py` that acts as an automated test. The script must:
   - Create a file named `mock_data.bin` in the same directory, containing exactly the ASCII string: `VERIFY_CHECKSUM_TEST_STRING` (no newline at the end).
   - Programmatically compute the CRC32 checksum of the contents of `mock_data.bin` using Python. Format it as a zero-padded 8-character lowercase hexadecimal string (e.g., `0a1b2c3d`).
   - Execute the compiled `./verifier` binary as a subprocess, passing `mock_data.bin` as the first argument and the computed hex checksum as the second argument.
   - If the subprocess exits with a success code (0), write the 8-character hex checksum to `/home/user/pr_review/test_result.log`. If it fails, write `FAILED` to the log.

Run `make` to ensure everything builds correctly, then run your `test_fixture.py` script to generate the log file.