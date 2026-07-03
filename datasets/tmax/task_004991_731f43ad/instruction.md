You are a systems programmer tasked with fixing and completing a C++ data sanitizer service. The service is part of a larger pipeline that validates encoded telemetry payloads.

Your workspace is located at `/home/user/workspace`. Inside, you will find:
- `start_services.sh`: A script that starts a local Redis instance (port 6379) and a Python Flask API (port 5000). You must run this script before testing your C++ code.
- `Makefile`: A broken build file for the C++ project.
- `src/`: The source code for the `telemetry_sanitizer` C++ application.
- `corpus/clean/`: A directory of valid telemetry files.
- `corpus/evil/`: A directory of invalid or malicious telemetry files.

The `telemetry_sanitizer` takes an input file and an output directory as arguments. It is supposed to do the following for each file:
1. Connect to the Flask API at `http://127.0.0.1:5000/config` to retrieve a JSON configuration containing a list of allowed CRC32 checksums.
2. Read the input file, which contains a Base64 encoded payload.
3. Decode the Base64 payload.
4. Verify that the decoded payload's CRC32 checksum (computed over the decoded bytes) is present in the allowed list from the Flask API.
5. Verify that the decoded payload is strictly valid UTF-8.
6. Log the filename and status to Redis (e.g., `INCR processed_files`).
7. If the file passes all checks, write the decoded UTF-8 payload to the output directory with the same filename. If it fails *any* check (invalid Base64, bad CRC32, invalid UTF-8), do not write the file to the output directory.

Your tasks:
1. **Fix the Build System**: The `Makefile` has a linking error. You must identify the missing dependencies (it uses `libcurl` and `hiredis`) and update the `Makefile` so that `make` successfully builds `bin/telemetry_sanitizer`. You may need to install the missing development packages via `apt`.
2. **Memory Debugging**: The provided Base64 decoding function in `src/decoder.cpp` has a memory corruption bug (buffer overflow/memory leak). Use memory debugging tools (like Valgrind or AddressSanitizer) to find and fix the bug.
3. **Implement the Filter**: Ensure the CRC32 and UTF-8 validation logic in `src/main.cpp` correctly implements the rules described above.
4. **Process the Corpus**: Create the directory `/home/user/workspace/out_clean`. Run your fixed `telemetry_sanitizer` on every file in both `/home/user/workspace/corpus/clean/` and `/home/user/workspace/corpus/evil/`, outputting the accepted files to `/home/user/workspace/out_clean/`.

An automated test will verify that:
- 100% of the files from the `clean` corpus are correctly decoded and written to `out_clean`.
- 0% of the files from the `evil` corpus are present in `out_clean`.
- The Redis counter `processed_files` matches the total number of files processed.