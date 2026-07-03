You are tasked with fixing a broken Go web security application located in `/home/user/sec-app`.

This application implements a rate-limiting middleware that also uses CGO to call a high-performance C library (`libtokencheck.so`) for token validation. The development team reported two main issues:

1. **Build/Linker Issue:** Running `make test` fails. The C library compiles correctly, and the Go code compiles, but the test binary fails to run because it cannot find the shared library `libtokencheck.so` at runtime. You need to fix this issue either by modifying the `#cgo` directives in the Go code or by updating the `Makefile`. Do not rely on manual shell exports; the `make test` command must work autonomously.
2. **Rate Limiting Logic Bug:** Once the linking issue is resolved, the tests will still fail. The `TestRateLimit` unit test asserts that the middleware should allow exactly 5 requests and return a `429 Too Many Requests` status on the 6th. However, there is a bug in the request validation logic in `middleware.go`. Fix the logic so the test passes.

Requirements:
- Ensure the application successfully links to the C library dynamically and the tests run when `make test` is executed.
- Correct the rate-limiting logic in `middleware.go`.
- The `Makefile`'s `test` target already redirects the test output to `/home/user/sec-app/test_results.log`. You must leave this redirect intact so that the automated verification can read `test_results.log`.
- Run `make test` to generate the passing `test_results.log` file.