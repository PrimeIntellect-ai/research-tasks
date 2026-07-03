You are a developer working on a Web Security log processing tool. The previous developer left the source files scattered in a flat directory without any build configuration, tests, or project structure. 

Your task is to organize these files into a structured monorepo, set up the FFI boundary between Go and Rust, write a property-based test, and create a CI/CD build script.

The scattered files are located in `/home/user/raw_source/`:
1. `analyzer.rs` - A Rust file containing a SQL injection heuristic function.
2. `main.go` - A Go file that parses a structured JSONL log file, spins up a pool of goroutines, and concurrently checks each log entry by calling the Rust library via CGO.
3. `logs.jsonl` - A sample dataset of structured web access logs.

Perform the following steps:

1. **Project Organization:**
   Create a new directory `/home/user/sec_logger/`.
   Inside it, create two sub-projects: `rust_lib` (a Rust library) and `go_cli` (a Go application).
   Move `analyzer.rs` into the appropriate `src` directory in `rust_lib` (rename it to `lib.rs`).
   Move `main.go` into `go_cli`.
   Move `logs.jsonl` into `/home/user/sec_logger/`.

2. **Rust Library & Property Testing:**
   Initialize `rust_lib` as a Cargo library. Configure it to compile as a static library (`staticlib`) so Go can link to it.
   The `lib.rs` file contains a function `pub extern "C" fn analyze_payload(c_str: *const c_char) -> bool`.
   Add `proptest` as a dev-dependency. Write a property-based test in `lib.rs` that generates arbitrary random strings and asserts that calling the underlying Rust string parsing logic (you will need to write a safe wrapper/internal function for the C-string pointer) never panics.

3. **Go Concurrency & FFI Setup:**
   Initialize a Go module in `go_cli` (e.g., `go mod init sec_logger/cli`).
   Modify `main.go` to correctly link against the compiled `librust_lib.a` using CGO directives (`LDFLAGS: -L../rust_lib/target/release -lrust_lib` and ensure `-ldl -lm` are present if needed).
   Ensure the Go code correctly sets up a worker pool using goroutines and channels to parse the JSON logs and pass the `"payload"` field to the Rust FFI.

4. **CI/CD Pipeline:**
   Create a bash script at `/home/user/sec_logger/ci_build.sh`.
   This script must:
   - Have executable permissions (`+x`).
   - Run the Rust property-based tests (`cargo test` inside `rust_lib`).
   - Build the Rust library in release mode.
   - Build the Go application (`go build -o scanner` inside `go_cli`).
   - Run the compiled Go application against `../logs.jsonl`.
   - Redirect the standard output of the Go application to `/home/user/sec_logger/final_report.txt`.

Ensure your CI script stops and exits with a non-zero code if any step fails (e.g., using `set -e`). Do not use any external frameworks for CI (like GitHub Actions); the bash script itself is the pipeline.