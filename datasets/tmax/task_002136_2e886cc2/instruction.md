You need to build a system consisting of a Rust shared library for numerical computation and a Go web server that wraps it. You have been provided with a partially completed workspace.

Your tasks are:

1. **Fix the Rust Library**:
   - The Rust library is located in `/home/user/rust_lib`. It implements a C ABI function `poly_eval` to evaluate a polynomial.
   - Currently, it fails to compile due to a Rust borrow checker/ownership bug in `/home/user/rust_lib/src/lib.rs`.
   - Fix the bug so that the library compiles successfully as a `cdylib` without changing the function signature or the mathematical logic.
   - Build the Rust library in release mode.

2. **Develop the Go Web Server**:
   - In `/home/user/go_app`, write a Go web server (`main.go`) that links to the Rust shared library via `cgo`.
   - The server must expose a `POST /compute` endpoint.
   - The endpoint expects a JSON payload: `{"coeffs": [a_n, a_{n-1}, ..., a_0], "x": value}` where `coeffs` is an array of float64 and `x` is a float64.
   - It should call the Rust `poly_eval` function and return a JSON response: `{"result": value}`.
   - **Validation**: If `coeffs` is empty or missing, return an HTTP 400 Bad Request.
   - **Rate Limiting**: Implement a rate limiter that allows a maximum of 2 requests per IP address per second. Exceeding this should return an HTTP 429 Too Many Requests.

3. **Write Go Tests**:
   - Write unit/integration tests in `/home/user/go_app/main_test.go` that test:
     a) A successful calculation.
     b) The request validation (empty `coeffs`).
     c) The rate limiter (triggering a 429 response by sending 3 rapid requests).

4. **Build the Go binary**:
   - Compile the Go application to `/home/user/go_app/server`.
   - Ensure that the binary can run successfully and locate the Rust shared library (e.g., using `-Wl,-rpath` in your cgo LDFLAGS).

Ensure your Go code is well-formatted and passes your tests (`go test`). Do not change the `C` function signature `double poly_eval(const double* coeffs, size_t len, double x)`.