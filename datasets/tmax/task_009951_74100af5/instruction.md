You are a platform engineer troubleshooting a failing CI pipeline for a hybrid Go/C project. 

Our numerical processing library has a core algorithm written in C for performance, with a Go wrapper and test suite. The tests pass locally when developers run a standard `go test`, but they are failing sporadically and triggering race conditions in our CI environment where tests are run with `go test -race`.

The CI logs indicate a data race in the C code when property-based tests are executed concurrently. 

Your task:
1. Navigate to `/home/user/numeric-lib`.
2. Analyze the Go test suite (`num_test.go`) and the underlying C implementation (`algo.c`, `algo.h`).
3. Fix the C code in `algo.c` to be thread-safe. Do NOT change the function signatures in `algo.h`, as other downstream systems depend on this ABI.
4. Verify your fix by running `go test -race` in the directory.
5. Once the tests pass without any race conditions, redirect the successful output of `go test -race` to `/home/user/test_results.log`.

The automated verification will check that `/home/user/test_results.log` exists, contains the passing test output, and that `algo.c` compiles and is free of global state race conditions.