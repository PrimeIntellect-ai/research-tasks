You are a platform engineer responsible for maintaining CI/CD pipelines. Our latest build for the `mathvm` project is failing. 

The `mathvm` project implements a high-performance mathematical expression evaluator (a simple stack-based virtual machine) in C, wrapped in Go via `cgo`. The CI pipeline uses Go's property-based testing (`testing/quick`) to generate random mathematical operations and ensure our C VM produces the exact same results as Go's standard `math` library.

Currently, the pipeline fails for multiple reasons:
1. The `Makefile` is broken and fails to produce the shared library `libmathvm.so`.
2. Even when compiled, the Go property-based tests catch a severe mathematical logic error in the C implementation (`vm.c`) regarding the subtraction operation.
3. The environment is missing the proper configuration to link the `.so` file at runtime during `go test`.

Your task is to fix the workspace located at `/home/user/math-ci`:
1. Repair the `Makefile` so that running `make` successfully produces `libmathvm.so`.
2. Identify and fix the logic bug in `vm.c`.
3. Ensure that running `go test -v` passes completely.
4. Once the tests pass, create a file at `/home/user/math-ci/success.log` containing exactly the text `CI_PIPELINE_FIXED`.

Note: You may need to set environment variables (like `LD_LIBRARY_PATH`) in your terminal session to allow `go test` to run against the newly built shared library in that directory.