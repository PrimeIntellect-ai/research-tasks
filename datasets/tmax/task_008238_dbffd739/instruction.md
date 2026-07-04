You are a mobile build engineer maintaining a C-based pipeline. Your automated build has failed due to a linkage error and a logic bug introduced by a recent schema migration.

The project is located at `/home/user/pipeline`. 

Here is what you need to do:
1. **Fix Linkage:** The `CMakeLists.txt` builds an executable `mobile_test`, but it fails at link time because it cannot find the `device_proto` shared library. This precompiled shared library is located in `/home/user/pipeline/vendor/lib`. Modify `CMakeLists.txt` to properly link this directory so the build succeeds. Also ensure the executable can find the shared library at runtime (e.g., using RPATH in CMake or setting environment variables during execution).
2. **Fix State Machine:** The file `src/parser.c` contains a state machine constraint bug. It is supposed to transition state `0 -> 1 -> 2 -> 3` for events `1`, `2`, and `3` respectively. However, event `3` incorrectly transitions to an error state (`-1`). 
3. **Generate Patch:** Before fixing the file, generate a unified diff patch that corrects `src/parser.c`. Save this patch exactly as `/home/user/pipeline/parser.patch`. Then apply your patch.
4. **Build and Test:** Create a `build` directory inside `/home/user/pipeline`, compile the project using `cmake .. && make`, and execute `./mobile_test`.
5. **Log Output:** Redirect the standard output of the successful test run to `/home/user/test_result.log`.

The automated verification will check that the build succeeds, the patch exists and is valid, and the `test_result.log` contains the expected success message.