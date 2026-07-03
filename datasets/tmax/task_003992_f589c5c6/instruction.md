You are an open-source maintainer reviewing a broken Pull Request (PR #104) for our Bash-based mathematical microservice. The PR attempts to integrate a highly optimized C library for modular arithmetic by wrapping it in a custom Bash loadable builtin. The goal is to run a TCP server purely in Bash that answers mathematical queries using this native C library.

Unfortunately, the PR author left several issues:
1. They vendored the math library at `/app/libmathops-1.2.0`, but the project's build system (a simple Makefile) fails to link the shared library properly because it is missing a critical compiler flag required for shared objects.
2. The Bash builtin code located at `/app/pr-104/` has a C memory leak in its primary execution path. When the builtin executes, it fails to free a dynamically allocated string returned by the library.
3. The PR lacks the actual Bash script to run the TCP server.

Your task:
1. **Fix the Vendored Library:** Navigate to `/app/libmathops-1.2.0` and fix the `Makefile` so that running `make` successfully compiles `libmathops.so`.
2. **Fix and Build the Builtin:** Navigate to `/app/pr-104`. Fix the memory leak in `fibfast.c` (look for a missing `free()` for the string returned by `compute_fib`). Then run `make` to build the Bash loadable builtin `fibfast.so`.
3. **Write the Server Script:** Create a Bash script at `/home/user/server.sh`. The script must:
   - Load the compiled builtin using `enable -f /app/pr-104/fibfast.so fibfast`.
   - Ensure the runtime linker can find `libmathops.so` (e.g., by exporting `LD_LIBRARY_PATH=/app/libmathops-1.2.0`).
   - Listen on TCP port `9090` (you may use `socat` or similar shell utilities).
   - For every incoming line of data, parse it as a JSON object: `{"n": <integer>, "mod": <integer>}`.
   - Execute the builtin: `fibfast <n> <mod>` (this builtin echoes the string result to stdout).
   - Return a JSON object to the client: `{"result": <integer>}` followed by a newline.
4. **Run the Server:** Execute `/home/user/server.sh` in the background so it is listening on `127.0.0.1:9090`.

Ensure the server is running, does not leak memory over repeated calls (which would eventually crash the wrapper), and correctly parses and outputs the exact JSON structures requested.