You are an open-source maintainer reviewing a broken Pull Request for `SafeHashed`, a C++ backend service that calculates and compares checksums for web security auditing. 

A contributor submitted a PR to refactor the project. They attempted to extract the checksum algorithms into a dynamically loaded shared library (`libchecksum.so`) and added a new REST API endpoint to diff two sets of checksums. However, the PR is completely broken: it fails to build, fails to link, and the diffing logic has a bug.

The project is located at `/home/user/project`.

Your tasks:
1. **Fix the Build System & ABI**: 
   The `Makefile` in `/home/user/project` is broken. It fails to correctly compile the shared library and the main executable. Furthermore, `main.cpp` tries to load `libchecksum.so` dynamically using `dlopen` and `dlsym` to find the `calculate_checksum` function, but it fails due to C++ name mangling (ABI issue). Fix `src/checksum.cpp`, `src/checksum.h`, and the `Makefile` so that running `make` successfully builds `./libchecksum.so` and the `./safehashed` binary.
2. **Fix the Diff API**:
   The application uses `httplib.h` to serve a REST API on port 8080. The `/diff` endpoint takes two query parameters, `list_a` and `list_b` (comma-separated integers). It is supposed to sort them, perform a set difference (elements in A that are not in B), and return a JSON array. The current implementation in `src/main.cpp` is bugged and returns incorrect results. Fix the sorting and diffing logic.
3. **Verify**:
   - Run `make` in `/home/user/project` to build the fixed project.
   - Start `./safehashed` in the background.
   - Use `curl` to send a GET request to `http://127.0.0.1:8080/diff?list_a=99,15,42,8,23&list_b=42,8,100` and save the exact output to `/home/user/api_test.log`.

Requirements:
- Do not change the function signature of `calculate_checksum` or the overall architecture.
- The `Makefile` must output the shared library to `libchecksum.so` and the executable to `safehashed`.
- Ensure your background process stays running so the `curl` command succeeds.
- The output in `/home/user/api_test.log` must be the raw JSON array string from the API (e.g., `[15, 23, 99]`).