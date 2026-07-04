You are a systems programmer managing the CI/CD pipeline for a high-performance web security router. The project uses a fast C library (`liburlsanitizer.so`) to perform security checks (like path traversal prevention) on URL routes, which is then utilized by bash scripts in our CI integration tests.

Currently, the CI pipeline is failing due to two issues:
1. **A C Library Linking Issue:** The script `/home/user/project/build.sh` is failing to properly compile and link the shared object and the wrapper binary `url_tool`. The C compiler complains about position-independent code, and even if you force the compilation, the resulting binary fails to find the shared object at runtime.
2. **URL Parameter Parsing Bug:** The bash integration test `/home/user/project/test_routing.sh` incorrectly parses URLs. It isolates the path but fails to strip off query parameters (anything after and including `?`), which causes the C security checker to evaluate the wrong string and fail the test harness.

Your task:
1. Fix `/home/user/project/build.sh` so that `liburlsanitizer.so` is built correctly and `url_tool` can be executed without failing to load the shared library. (Modify the build script so it handles the linking and runtime library resolution self-sufficiently without relying on the user setting environment variables prior to running).
2. Fix `/home/user/project/test_routing.sh` using Bash utilities so that it correctly strips query parameters from the extracted path before passing it to `url_tool`.
3. Run the CI pipeline by executing `/home/user/project/ci_run.sh`. If successful, this script will automatically generate `/home/user/project/ci_success.log`. 

The system is configured, and the files are waiting in `/home/user/project/`. Leave the `ci_success.log` file in place when you are finished.