You are a systems programmer debugging a C library linking issue and a memory leak in a semantic version processing tool. 

We have a vendored third-party package, `cJSON-1.7.15`, located at `/app/cJSON-1.7.15`. The Makefile for this library has a deliberate flaw: it fails to compile the shared library (`libcjson.so`) on modern Linux systems due to a missing Position Independent Code (PIC) flag on its object files, resulting in a linking error.

Additionally, in `/home/user/parser_app/`, there is a custom C program `semver_parser.c` that relies on this shared library. It reads a large JSON file of software versions (`/home/user/parser_app/versions.json`), parses the JSON array, and uses a custom state machine to parse and compare the semantic versions to find the highest valid version. However, `semver_parser.c` suffers from a massive memory leak.

Your tasks are:
1. **Fix the Linking Issue**: Modify the `/app/cJSON-1.7.15/Makefile` so that `libcjson.so` builds successfully. 
2. **Create a Patch**: Generate a unified diff of your Makefile fix and save it to `/home/user/cjson-fix.patch`.
3. **Fix the Memory Leak**: Debug and profile `/home/user/parser_app/semver_parser.c`. Fix the memory leaks (e.g., missing JSON object cleanup and un-freed state machine nodes).
4. **Build and Run**: Compile `semver_parser.c` as `semver_parser`, dynamically linking it against your newly built `libcjson.so`. Ensure the system can find the shared library at runtime.
5. **Output**: Run `./semver_parser /home/user/parser_app/versions.json`. It must output the highest semantic version it finds to `/home/user/highest_version.txt`.

We will verify your solution by running your compiled `semver_parser` under `valgrind` and parsing the memory profiling results. Your goal is to reduce the "definitely lost" bytes to absolutely zero.