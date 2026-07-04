You are tasked with fixing a vendored C++ web security component that is currently failing to compile and link. The package, `fast-url-router`, is designed to securely route HTTP requests by extracting the URL path, decoding a Base64-encoded payload parameter, and validating its integrity using a custom checksum algorithm.

The source code is provided as a vendored package located at `/app/fast-url-router-1.0.0/`.

Currently, the project fails to build due to compilation and linkage errors (specifically C/C++ ABI mismatches and shared library linking issues). Furthermore, the original developer left a note indicating that even if it compiles, there is a minor logical bug in the URL parameter parsing logic that causes incorrect checksum validations on certain payloads.

Your objectives are:
1. **Fix the Build System & ABI:** Inspect the `Makefile` and the headers. The project builds a shared library `libvalidator.so` (which contains an assembly-optimized checksum routine) and a main executable `fast_router`. Fix the linkage errors and ABI mismatch between the C++ routing code and the C validation library. Ensure the `Makefile` correctly links the shared library using an appropriate rpath so the binary can run independently.
2. **Fix the Routing Logic:** Inspect `router.cpp`. It extracts the `payload` query parameter from URLs (e.g., `/api/v1/data?payload=SGVsbG8=&checksum=1234`). Fix the bug in the Base64 decoding or parameter parsing logic so that the decoded payload is correctly passed to the validator.
3. **Produce the Final Executable:** The fixed `Makefile` must successfully build the executable when you run `make` inside `/app/fast-url-router-1.0.0/`.
4. **Deploy:** Copy the final, working executable to `/home/user/fast_router`. Ensure that the compiled `libvalidator.so` is accessible to the executable (e.g., via the rpath you configured, or by copying the `.so` to `/home/user/` if your rpath relies on the same directory).

The final binary `/home/user/fast_router` must take exactly one argument (a URL string) and print the routed path, decoded payload, and checksum validation result to standard output. Its behavior must be bit-exact equivalent to our reference implementation.

You may use whatever terminal tools you need (gdb, ldd, objdump, bash, python scripts) to debug the ABI and checksum algorithms.