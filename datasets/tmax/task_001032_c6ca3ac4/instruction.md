You are acting as a DevOps engineer troubleshooting an in-house log processing tool written in Go. The tool is supposed to read a CSV log file, extract metrics, and compute a converged statistical value for each line, then output the sum of these metrics. 

However, you are facing a multi-faceted problem:
1. **Build Failure:** The project fails to build or download dependencies. Another engineer mentioned they accidentally misconfigured the Go environment on this machine, but they left for the day. You need to diagnose and repair the environment misconfiguration so you can compile the project.
2. **Convergence Failure:** When you manage to build the tool, running it against the production log file (`/home/user/data/server.log`) causes it to hang indefinitely. It seems to get stuck in an infinite loop due to a convergence failure in its numerical algorithm when processing a specific, anomalous log entry.
3. **Regression:** To ensure this never happens again, you must construct a regression test for the specific function causing the issue.

**Your objectives:**
1. Navigate to `/home/user/logprocessor/`.
2. Diagnose and fix the build environment misconfiguration so `go build` works successfully.
3. Locate the mathematical convergence algorithm in `processor.go`. The function `ConvergeMetric(v float64) float64` implements a Newton-Raphson square root approximation. However, it fails to converge (infinite loop) if the input metric is negative. 
4. Modify `ConvergeMetric` so that if the input `v` is negative, it immediately returns `0.0` instead of looping.
5. Create a regression test file at `/home/user/logprocessor/processor_test.go`. Write a test function exactly named `TestConvergeMetric_Negative` that passes `-5.0` to `ConvergeMetric` and asserts that the return value is `0.0`. If it is not `0.0`, the test should fail using `t.Errorf`.
6. Build the fixed tool and place the compiled binary exactly at `/home/user/logprocessor/bin/logprocessor`.
7. Execute the compiled binary on `/home/user/data/server.log` and save its standard output (the final computed float) into `/home/user/result.txt`.

**Environment details:**
- Project directory: `/home/user/logprocessor`
- Production logs: `/home/user/data/server.log`
- All Go code you write must be properly formatted and use standard Go testing conventions.