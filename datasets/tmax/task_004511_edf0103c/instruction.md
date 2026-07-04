You are tasked with fixing and configuring the core C-based routing module for a new polyglot build system. This module, located at `/home/user/build_router`, intercepts build requests, parses their URLs, compares semantic versions to select the appropriate toolchain, and supports conditional cross-compilation builds.

Currently, the project has several issues:
1. **Makefile Repair & Conditional Builds**: The `Makefile` in `/home/user/build_router` is broken. It fails to compile the executable because of a linking error (missing object file mapping). Furthermore, you need to update the `Makefile` so that if you run `make ARCH=cross`, it appends `-DCROSS_COMPILE_MODE` to the `CFLAGS`. 
2. **Semantic Version Bug**: The version comparison logic in `semver.c` relies on naive string comparison, which causes bugs (e.g., version `1.10.0` is incorrectly evaluated as older than `1.2.0`). Modify `compare_versions()` in `semver.c` to properly parse and compare the major, minor, and patch integers. The function signature is `int compare_versions(const char* v1, const char* v2);` and it should return `1` if `v1 > v2`, `-1` if `v1 < v2`, and `0` if they are equal.
3. **URL Parsing**: The `url_parser.c` correctly extracts target architectures from strings like `build://project/1.2.3?arch=arm64`, but it causes a segmentation fault on malformed URLs missing the `?` character. Fix the segfault so it safely returns `NULL` for the architecture if `?arch=` is not present.

**Action Items:**
1. Fix the C source files (`semver.c` and `url_parser.c`) and the `Makefile`.
2. Compile the project normally using `make`.
3. Compile the project again to test the cross-compilation flag by running `make clean && make ARCH=cross`. The resulting binary should be named `router`.
4. Run the provided benchmark script `/home/user/build_router/benchmark.sh` which will feed 5,000 URLs to your compiled `./router` binary. Redirect the standard output of this script to `/home/user/benchmark_results.log`.
5. Verify your semantic version logic by running the following commands and saving their exact terminal output to `/home/user/version_tests.log`:
   - `./router semver 1.10.0 1.2.0`
   - `./router semver 2.0.0 2.0.0`
   - `./router semver 0.9.5 0.10.1`

Ensure all output files (`benchmark_results.log` and `version_tests.log`) are precisely created at the specified paths.