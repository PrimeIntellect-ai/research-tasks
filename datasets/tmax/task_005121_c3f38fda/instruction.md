You are a platform engineer maintaining the CI/CD pipelines for a high-performance mathematical computing library. The pipeline is currently failing due to memory safety issues in a core matrix computation module, and the reporting pipeline needs a reverse proxy configuration to route test results correctly.

Your objective is to complete the following three phases:

**Phase 1: Fix C Memory Safety and Generate a Patch**
In `/home/user/math_lib`, there is a C program `matrix_trace.c` that reads a matrix size `n` and an `n x n` matrix from standard input, dynamically allocates memory, and calculates the trace (sum of the main diagonal). However, it suffers from a segmentation fault due to undefined behavior (an off-by-one error) and a memory leak.
1. Fix the memory safety issues in `/home/user/math_lib/matrix_trace.c` without changing its core mathematical logic or input/output format.
2. Generate a unified diff patch file named `/home/user/math_lib/fix.patch` that contains the differences between the original `matrix_trace.c.orig` (which is already provided in the directory) and your fixed `matrix_trace.c`.

**Phase 2: Parse Structured Data and Run CI**
The CI pipeline uses a JSON file containing test vectors located at `/home/user/ci/test_vectors.json`.
1. Compile your fixed C program to `/home/user/math_lib/matrix_trace`.
2. Write a bash script at `/home/user/ci/run_tests.sh` that:
   - Uses `jq` to parse `/home/user/ci/test_vectors.json`. The JSON contains an array of objects, each with an `id`, `size`, and `matrix` (an array of integers).
   - Iterates through each test case.
   - For each test case, feeds the `size` followed by the `matrix` elements into the `matrix_trace` binary.
   - Collects the output (the trace value).
   - Outputs a new JSON array to `/home/user/ci/results.json` where each element is an object: `{"id": <id>, "trace": <calculated_trace>}`.
3. Run your script so that `/home/user/ci/results.json` is generated.

**Phase 3: Configure Reporting Reverse Proxy**
The CI system needs to report these results to a backend metrics server, but it must go through an internal proxy.
1. Create an unprivileged Nginx configuration file at `/home/user/ci/proxy.conf`.
2. The configuration must:
   - Run as the current user (do not use `user root;` or require sudo).
   - Store its pid file at `/home/user/ci/nginx.pid`.
   - Store error and access logs at `/home/user/ci/error.log` and `/home/user/ci/access.log`.
   - Set up an HTTP server listening on `127.0.0.1:8080`.
   - Act as a reverse proxy: any requests to the path `/report` must be proxied to the upstream backend server at `http://127.0.0.1:9090`.

Ensure all file paths are exact and your bash script `/home/user/ci/run_tests.sh` is executable. You do not need to start Nginx, but your configuration must be syntactically valid (we will test it using `nginx -t -c /home/user/ci/proxy.conf`).