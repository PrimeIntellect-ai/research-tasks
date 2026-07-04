You are a DevOps engineer tasked with debugging a critical log-analysis utility written in Go. The source code is located in `/home/user/metric-calc`. 

The utility calculates a "Server Health Score" based on access log metrics. However, the latest commit on the `master` branch is broken in two ways:
1. It currently fails to compile due to a syntax/linker error.
2. The health score calculation was reported to be producing incorrect results compared to the known-good release tag `v1.0`.

Your task:
1. Fix the compilation error in `main.go` on the current `master` branch so that the program builds.
2. Use `git bisect` (or manual bisection) between the `v1.0` tag and the original broken `master` branch to find the exact commit that introduced the logic regression in the health score formula.
3. Write ONLY the full 40-character commit hash of the bad commit to `/home/user/bad_commit.sha`.
4. Correct the formula implementation in `main.go`. The correct formula for the health score is: `((Success - Failed) / Total) * 100` (returned as a float64).
5. Ensure that `go test` passes successfully.
6. Build the corrected Go application and output the executable to `/home/user/metric-calc/calc`.

Do not modify the test file `main_test.go`. Focus purely on fixing `main.go` and identifying the regression.