You are a mobile build engineer troubleshooting a CI pipeline issue. A project compiles and runs fine locally but fails in the CI environment due to unpredictable linking order of shared libraries.

The project relies on two shared libraries that perform mathematical operations. Both accidentally export a mathematically identical function signature, causing symbol clashes (ABI conflicts). Depending on the environment, the main application picks up the wrong function and produces incorrect mathematical results.

Your task is to:
1. Identify the conflicting symbols.
2. Fix the shared library build process to manage the ABI.
3. Serve the result of the fixed application via a simple Bash-based REST API.

Here are the details:

**Directory Setup:**
Work in `/home/user/mobile_build`. You will find:
- `libmath_alpha.c`: Contains a mathematical function `int calculate_metric(int input)` that returns `input * 2`.
- `libmath_beta.c`: Also contains `int calculate_metric(int input)` but returns `input * input`. It also contains `int beta_specific_math()`.
- `main.c`: Calls `calculate_metric(5)`.
- `build.sh`: A broken build script.

**Step 1: Sort, Merge, and Diff**
Use `nm` on the compiled `libmath_alpha.so` and `libmath_beta.so` (after running the current `build.sh` once) to extract their exported dynamic symbols (`nm -D --defined-only`). Find the symbols that are exported by *both* libraries. Sort the overlapping symbol names alphabetically and save them to `/home/user/mobile_build/conflict.txt` (one symbol per line).

**Step 2: Shared Library and ABI Management**
The application is expected to output `10` (meaning it must use `calculate_metric` from `libmath_alpha.so`).
Modify `build.sh`. To prevent this CI linker order issue permanently, you must use a linker version script named `beta.map` (which you need to create) when compiling `libmath_beta.so`. The version script should make `calculate_metric` local (hidden) in `libmath_beta.so`, while keeping `beta_specific_math` global.
Ensure `build.sh` compiles the `.so` files, applies the version script to beta, and compiles `./app` linking against both (using `-Wl,-rpath=. -L. -lmath_alpha -lmath_beta`).

**Step 3: REST API Construction**
Create a Bash script at `/home/user/mobile_build/api.sh` that implements a simple HTTP server using `nc` (netcat). 
The server must listen on port `8080`.
When it receives an HTTP `GET /api/math/result` request, it should execute `./app`, capture its integer output, and respond with a `200 OK` HTTP status and the JSON payload:
`{"status": "success", "result": <APP_OUTPUT>}`
(e.g., `{"status": "success", "result": 10}`).
Ensure the script runs continuously (e.g., using a `while true` loop). You can start it in the background to verify it works.

**Verification:**
- `/home/user/mobile_build/conflict.txt` must contain exactly the conflicting symbol.
- Running `./build.sh` must succeed and yield an `./app` that prints `10`.
- Your bash server on port 8080 must respond correctly to `curl http://localhost:8080/api/math/result`.