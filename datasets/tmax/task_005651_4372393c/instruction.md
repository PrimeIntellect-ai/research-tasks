You are a mobile build engineer maintaining the build pipelines for a cross-platform application. We have a pre-launch validation step that currently runs as a Python script, but we need to run it directly on the target devices (Linux x86_64 and Android ARM64) where Python is not available.

Your task is to:
1. Translate the validation logic from `/home/user/validator.py` into a compiled language of your choice (e.g., C, C++, Go, Rust). The validator checks a custom binary structure:
   - Magic Header (4 bytes): "MOBI" (`0x4D, 0x4F, 0x42, 0x49`)
   - Version (2 bytes, Little Endian): Must be `1`
   - Payload Size (4 bytes, Little Endian): `N`
   - Payload (`N` bytes)
   - Checksum (1 byte): The XOR sum of all bytes in the Payload.
   - The total file size must be exactly `10 + N + 1` bytes.

2. Write the compiled program to take a single command-line argument: the path to the binary file to validate. It must exit with status `0` if the file is valid, and status `1` if it is invalid.

3. Cross-compile your program to create two statically-linked, stripped binaries:
   - `/home/user/validator_x86` (for x86_64 Linux)
   - `/home/user/validator_arm64` (for aarch64 Linux)
   *(Hint: You can use Go with `GOARCH=arm64` and `GOARCH=amd64` and `CGO_ENABLED=0`, or download a local toolchain like Zig if you prefer C/C++).*

4. Write a bash script `/home/user/run_tests.sh` that:
   - Executes `/home/user/validator_x86` on `/home/user/valid.bin`.
   - Executes `/home/user/validator_x86` on `/home/user/invalid.bin`.
   - Writes the exact exit codes to `/home/user/test_results.log` in this exact format:
     ```
     valid_exit: <code for valid>
     invalid_exit: <code for invalid>
     ```

We have placed the Python reference script and the test files in `/home/user/`.