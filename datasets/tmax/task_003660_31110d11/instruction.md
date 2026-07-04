I need you to build a polyglot mathematical processing system from scratch. We have a high-performance Rust library for calculating the "Sum of Divisors" (Sigma function) for large integers, and we need a Go application to process a large dataset concurrently using this library.

Here is the current state of the system and what you need to do:

1. **Vendored Rust Library (`/app/divsum-0.1.0`)**:
   We have vendored the `divsum` library source. However, the previous developer left it in a broken state. It currently fails to compile due to a Rust borrow checker error in `src/lib.rs`. Additionally, the build system is not configured to output a C-compatible shared library (`.so`). 
   - Fix the Rust borrow checker issue.
   - Configure `Cargo.toml` to build a `cdylib`.
   - Build the shared library.

2. **Go Worker Application (`/app/go-worker`)**:
   Initialize a new Go module in `/app/go-worker`. Write a Go program (`main.go`) that:
   - Uses CGO to link against the compiled Rust `divsum` shared library.
   - Reads an input file located at `/app/input.json` (which contains a JSON array of `uint64` numbers).
   - Deserializes the JSON and processes each number by calling the Rust FFI function `sum_of_divisors`.
   - Implements **Go concurrency patterns** (goroutines and channels) to process the numbers concurrently.
   - Implements a strict **rate limiter/semaphore** to ensure no more than **4** concurrent FFI calls to the Rust library happen at the same time.
   - Serializes the results into a JSON map (where keys are the string representation of the input number, and values are the computed sum of divisors) and writes it to `/app/output.json`.

3. **Build System**:
   Create a `Makefile` in `/app` with a `build` target that handles compiling both the Rust library and the Go binary (outputting the Go binary to `/app/bin/worker`). Ensure all necessary linking flags (e.g., `CGO_LDFLAGS`, `LD_LIBRARY_PATH`) are properly configured so the Go binary can find the Rust `.so` file at runtime.

The output JSON will be evaluated for exact mathematical accuracy, and the Go binary will be evaluated for its concurrent performance speedup compared to a serial baseline. 

Please execute the necessary commands to fix the Rust code, write the Go code, and compile the final binary.