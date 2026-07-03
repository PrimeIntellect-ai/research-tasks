You are a systems programmer working on the CI/CD pipeline for a new Go-based Web Application Firewall (WAF) that leverages a high-performance C library for payload parsing. 

Currently, the project is broken. The Go modules have a circular import, the C library has a memory safety vulnerability (buffer overflow), and the CI/CD Bash script is missing.

Your task is to fix the codebase and write the CI/CD pipeline script.

Here is the current structure in `/home/user/waf/`:
- `db/`: Contains `v1_init.sql` and `v2_update.sql`.
- `c_src/parser.c`: The C library source.
- `c_src/parser.h`: The C library header.
- `go_src/main.go`: The main Go application.
- `go_src/engine/engine.go`: The evaluation engine.
- `go_src/config/config.go`: The configuration module.

**Step 1: Code Fixes**
1. **Go Circular Import:** `go_src/engine/engine.go` and `go_src/config/config.go` import each other. Refactor the code to break this circular dependency. The `config` package should define the `Rule` struct, and `engine` should use it without `config` needing to import `engine`.
2. **C Memory Safety:** `c_src/parser.c` contains a function `char* extract_payload(const char* input)` that has a buffer overflow vulnerability (it uses `strcpy` into a fixed 16-byte buffer). Fix it by allocating the exact required length (+1 for null terminator) using `malloc`.

**Step 2: Schema Migration & CI/CD Pipeline**
Write a Bash script at `/home/user/run_ci.sh` that automates the build and testing. The script must:
1. Ensure the script fails immediately if any command fails (`set -e`).
2. Run the database schema migrations by applying `db/v1_init.sql` followed by `db/v2_update.sql` to a new SQLite database at `/home/user/waf/waf.db`.
3. Compile the C code (`/home/user/waf/c_src/parser.c`) into a shared library named `libparser.so` in the `/home/user/waf/` directory. You must compile it with AddressSanitizer enabled (`-fsanitize=address`) and Position Independent Code (`-fPIC`).
4. Build the Go application in `/home/user/waf/go_src/` into an executable named `waf_binary` located in `/home/user/waf/`. Note: You will need to pass the appropriate `CGO_LDFLAGS` and `CGO_CFLAGS` so it can find `libparser.so` and `parser.h`.
5. Run the compiled `waf_binary` with the argument `"DROP TABLE users;"` and redirect its standard output to `/home/user/waf/test_report.txt`. Ensure the `LD_LIBRARY_PATH` is set so the Go binary can find `libparser.so` at runtime.

Ensure `/home/user/run_ci.sh` is executable. You may modify the C and Go files directly using command-line tools before or while writing the script.