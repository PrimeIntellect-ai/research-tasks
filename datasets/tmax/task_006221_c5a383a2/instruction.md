**PagerDuty Alert - 03:14 AM - CRITICAL: Data Processing CI/CD Pipeline Broken**

Wake up. We have a severe incident with the new `vwap-calculator` microservice. A recent merge broke the CI/CD pipeline, and the background job cannot be deployed. This service is responsible for computing the Volume-Weighted Average Price (VWAP) for our financial datasets, and downstream systems are stalling.

Here is the situation:
1. **Build Failure**: The project is located at `/home/user/oncall/vwap`. Running `go build` or `go test` currently fails with a compiler/linker error. 
2. **Intermittent Test Failures**: Before the build completely broke, the CI reported that `go test` was occasionally failing with an assertion error. You'll need to reproduce this intermittent failure (try running the tests multiple times in a row).
3. **Bad Math & Precision**: The downstream consumers reported that before the pipeline broke, the VWAP values looked completely incorrect for highly skewed datasets (e.g., very large prices mixed with small ones). There is likely a bug in the formula implementation itself, as well as a floating-point precision issue causing data loss during accumulation.

**Your Objectives:**
1. Fix the compiler/linker error preventing the package from building.
2. Fix the formula implementation in `vwap.go` to correctly calculate the Volume-Weighted Average Price. The standard VWAP formula is: `Sum(Price * Volume) / Sum(Volume)`.
3. Repair the floating-point precision issue so the test assertion passes reliably, even for large numbers. You may change internal variable types, but **do not change the exported function signature** (`func ComputeVWAP(prices []float32, volumes []float32) float32`).
4. Ensure `go test -count=50` passes consistently without any assertion failures.
5. Create a file at `/home/user/result.txt` containing the exact string output of running your fixed `ComputeVWAP` function with the following inputs:
   `prices = []float32{10000000.0, 100.0, 105.0}`
   `volumes = []float32{1.0, 500000.0, 600000.0}`
   Format the output to 4 decimal places (e.g., using `fmt.Sprintf("%.4f", result)`).

Get this fixed as soon as possible so we can unblock the deployment.