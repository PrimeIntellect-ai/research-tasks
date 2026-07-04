I need you to debug a memory leak in a long-running mathematical service written in Go. We have a vendored version of the source code located at `/app/math-service`. 

Currently, when the service runs, it consumes memory linearly until it crashes. We believe a regression was introduced recently, but the `Makefile` and environment seem to have been misconfigured, preventing us from properly building and profiling the application.

Your task:
1. Fix the environment/Makefile misconfiguration in `/app/math-service` so that it builds correctly.
2. Identify the root cause of the memory leak (it has something to do with how we cache intermediate mathematical results).
3. Fix the memory leak in the Go source code.
4. Compile the fixed service and output the binary to `/home/user/math-service-fixed`.

The automated test will run `/home/user/math-service-fixed` with a load generator for 50,000 requests. To pass, the service's maximum heap allocation (as measured by Go's runtime memory stats) must not exceed 50 MB during the run.