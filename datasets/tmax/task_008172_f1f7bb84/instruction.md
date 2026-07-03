You are helping migrate a legacy project that recently transitioned its data generation scripts from Python 2 to Python 3. The new Python 3 scripts generate a binary configuration file (`/home/user/workspace/config.bin`) using Protocol Buffers.

We have a C program in `/home/user/workspace` that reads this file, extracts a semantic version and a payload, and processes it. However, the project is currently broken in a few ways:

1. **Linker Error:** The project uses CMake, but `make` fails at link time. The C application cannot find the `protobuf-c` shared library symbols. 
2. **Semantic Versioning Bug:** The application uses a custom `semver_compare` function in `main.c` to check if the protobuf's `version` string is greater than or equal to `"2.0.0"`. The current implementation is broken (it just uses `strcmp`, which incorrectly evaluates `"2.10.0"` against `"2.2.0"`).
3. **Data Encoding:** The extracted `payload` (bytes) from the protobuf message is actually a Base64 encoded string, but the C code currently just writes the raw Base64 bytes to the output file.

Your tasks:
1. Fix the `CMakeLists.txt` so the project successfully compiles and links.
2. Fix the `semver_compare` function in `main.c` to correctly parse and compare semantic version strings (e.g., `MAJOR.MINOR.PATCH`). It should return 1 if `v1 > v2`, -1 if `v1 < v2`, and 0 if `v1 == v2`.
3. Modify `main.c` so that if the extracted version is `>= 2.0.0`, it decodes the Base64 `payload` and writes the decoded ASCII string exactly to `/home/user/result.log`. If the version is `< 2.0.0`, it should write `"VERSION_TOO_OLD"` to `/home/user/result.log`.

The protobuf definition (`config.proto`), the generated `config.bin`, `main.c`, and `CMakeLists.txt` are provided in `/home/user/workspace`. 
Make the necessary code changes, build the application, and run it passing `config.bin` as the first argument to produce `/home/user/result.log`.

Note: You can use `apt-get` to install standard packages like `libprotobuf-c-dev` and `protobuf-c-compiler` if they are not already installed or if you need utilities. You must not change the protobuf definition.