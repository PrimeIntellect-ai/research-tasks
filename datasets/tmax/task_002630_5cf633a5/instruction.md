You are a systems programmer working on a distributed mathematical evaluation engine. The system comprises three services:
1. A Redis cache.
2. A high-performance C-based evaluation backend (`c_eval`).
3. A Go-based API gateway and expression sanitizer (`gateway`).

Currently, the system is broken in two major ways. First, the C backend is failing to compile and link due to a Makefile and dynamic linking issue. Second, the Go gateway lacks a robust expression sanitizer, making the C backend vulnerable to malicious mathematical expressions (such as division by zero, recursive constraint violations, and buffer overflows).

Your tasks are to:

1. **Fix the C Backend Build:**
   Navigate to `/home/user/app/c_eval`. There is a shared library `libmatheval.so` and a main server executable `eval_server`. The `Makefile` is broken—it fails to correctly link the shared library and setup the runtime path. Fix the `Makefile` and any dynamic linking issues so that running `make` successfully builds `eval_server`, and running `./eval_server` starts the backend on port 8081 without `cannot open shared object file` errors.

2. **Implement the Go Sanitizer:**
   Navigate to `/home/user/app/gateway`. You will find a file `sanitizer.go` containing an empty function:
   `func Sanitize(expr string) error`
   You must implement this function. It should parse and validate mathematical expressions.
   An expression is invalid (should return an error) if it:
   - Contains division by zero (e.g., `5 / 0`, `12 / (2 - 2)`).
   - Uses variables or unrecognized symbols (only numbers, `+`, `-`, `*`, `/`, `(`, `)` are allowed).
   - Has mismatched parentheses.
   An expression is valid (returns `nil`) if it is a strictly valid arithmetic expression obeying the above constraints.

3. **Multi-Service Composition:**
   Once both components are fixed, you must start the end-to-end system.
   - Start a local Redis server on the default port (6379).
   - Start the C backend `./eval_server` (listening on port 8081).
   - Start the Go gateway `go run main.go sanitizer.go` (listening on port 8080).

4. **Verification via Adversarial Corpus:**
   Inside `/home/user/app/corpora/`, there are two directories: `clean/` and `evil/`.
   Each contains `.expr` files. 
   When your system is running, sending a POST request to `http://localhost:8080/eval` with the raw text of a `.expr` file as the body should return an HTTP 200 OK (with the evaluated result) for all expressions in `clean/`, and an HTTP 400 Bad Request for all expressions in `evil/`.
   
You must leave all three services running in the background. Finally, create a log file at `/home/user/app/success.log` containing the text "READY" once the system is fully configured and running.