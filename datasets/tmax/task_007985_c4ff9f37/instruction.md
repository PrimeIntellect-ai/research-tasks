You are an integration developer responsible for testing a local data-processing API client.

You have been given a workspace at `/home/user/api_workspace` containing three files:
1. `payload.dat`: A mock API response payload.
2. `api_tester.c`: A C program designed to read a file, calculate its CRC32 checksum using zlib, and print the checksum in hex format. However, it currently contains a severe C memory safety bug (use-after-free) and crashes.
3. `build.sh`: A Bash script meant to compile `api_tester.c`, but it currently fails due to build system/linking errors.

Your task:
1. Fix the build system configuration in `build.sh` so that `api_tester.c` compiles successfully into an executable named `api_tester`.
2. Repair the C memory safety issue in `api_tester.c` so that it calculates the checksum accurately without crashing or causing undefined behavior. 
3. Create a Bash script at `/home/user/api_workspace/run_tests.sh` that:
   - Executes `./build.sh` to compile the client.
   - Runs `./api_tester payload.dat`.
   - Captures the standard output (which should be just the 8-character hex checksum, e.g., `a1b2c3d4`) and writes it to `/home/user/test_results.log`.

Requirements:
- Ensure `run_tests.sh` has executable permissions.
- The output in `/home/user/test_results.log` must contain ONLY the valid CRC32 checksum of the payload data.
- Do not modify `payload.dat`.