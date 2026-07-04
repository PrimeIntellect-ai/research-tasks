You are a mobile build engineer managing a CI/CD pipeline. Our custom C-based deep-link URL router located at `/home/user/router` is causing CI failures. It reportedly builds and passes tests locally on the developer's macOS machine, but it fails to compile on our Linux CI runners. Furthermore, a developer noted that there is a bug in the URL parser's state machine that causes tests to fail even when properly compiled.

Your tasks are to:
1. Fix the build issue in `/home/user/router/Makefile` so that `make` succeeds. The issue is likely related to the order of linker arguments.
2. Debug and fix the URL parsing state machine in `/home/user/router/deeplink_router.c`. The router is failing to extract query parameters correctly from deep links like `app://profile?id=123`. Ensure that running `./router test` prints `ALL TESTS PASSED` and exits with code 0.
3. Run the performance benchmark. Execute `/home/user/router/benchmark.sh` and redirect its standard output to `/home/user/benchmark_result.txt`. Note: Ensure you capture only the standard output in the file, not the timing statistics written to stderr.

Complete these steps in the terminal.