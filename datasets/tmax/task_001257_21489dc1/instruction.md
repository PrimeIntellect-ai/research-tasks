You are tasked with building a polyglot mathematical service that evaluates high-degree polynomials. We have an existing legacy C library that is supposed to perform the evaluation, but it is known to crash and leak memory under certain conditions. 

Your objectives are:
1. **Fix the C Library**: Under `/app/src/libpoly/`, there are two files: `poly.c` and `poly.h`. The `evaluate_polynomial` function has memory leaks and undefined behavior (buffer overreads/underreads). Debug and fix these memory safety issues. You may use Valgrind or AddressSanitizer.
2. **Build System**: Create a `Makefile` in `/app/` that builds `libpoly.so` as a shared library and compiles a Go binary named `poly-server`.
3. **CGO Integration & Unit Testing**: In `/app/src/go-server/`, write a Go package that uses CGO to interface with the fixed `libpoly.so`. Write a Go unit test (`poly_test.go`) that fuzzes or tests your CGO wrapper against the reference oracle binary located at `/app/poly_oracle`. This stripped binary takes arguments: `/app/poly_oracle <x> <a0> <a1> ... <an>` and prints the float result to stdout. Your tests must verify that your wrapper's output matches the oracle.
4. **HTTP Service**: Implement a Go web server in `/app/src/go-server/main.go` that:
   - Listens on exactly `127.0.0.1:8080`.
   - Exposes a `POST /poly/eval` endpoint.
   - Requires an `Authorization: Bearer SIGMA_7781` header.
   - Accepts a JSON payload: `{"coeffs": [1.5, 2.0, 3.1], "x": 2.0}` (where `coeffs` is an array of floats `[a0, a1, ..., an]`).
   - Returns a JSON response: `{"result": 17.9}`.
   - Calls your CGO wrapper to compute the result.

Ensure the Go server is built and running in the background listening on `127.0.0.1:8080` when you consider the task complete. The server must remain running. Do not use external Go web frameworks; use the standard `net/http` library.