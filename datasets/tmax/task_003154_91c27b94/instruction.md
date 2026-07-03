You are a DevOps engineer tasked with resolving a severe production issue. Our custom high-performance log anomaly detection library, `liblog-anomaly` (written in C), has been randomly hanging and consuming 100% CPU on certain log streams. 

The source code for this tool is vendored at `/app/vendored/liblog-anomaly`. It is managed as a local Git repository. 

Your task consists of three phases:

**Phase 1: Secret Recovery**
Our CI pipeline requires a legacy test API key to mock the log intake sink. This key was accidentally hardcoded in an older commit in the `liblog-anomaly` repository and later deleted. 
1. Perform Git forensics within `/app/vendored/liblog-anomaly` to recover the 16-character alphanumeric API key.
2. Save this key exactly as a single line in `/home/user/api_key.txt`.

**Phase 2: Delta Debugging & Isolation**
The file `/app/data/crash_logs.txt` contains 10,000 log lines. Processing this file causes the `anomaly_detector` binary to hang due to an infinite loop (convergence failure).
1. Use test minimization / delta debugging techniques to isolate the **single exact log line** that triggers the hang.
2. Save this exact single line into `/home/user/trigger_log.txt`.

**Phase 3: Convergence Repair & Optimization**
1. Inspect the C source code in `/app/vendored/liblog-anomaly/src/`. You will find that the clustering algorithm fails to converge on the specific data profile of the trigger log due to a strict floating-point equality check in the main loop.
2. Modify the code to use an epsilon-based convergence threshold (`1e-5`) instead of strict equality. 
3. Recompile the binary by running `make` in the `/app/vendored/liblog-anomaly/` directory.

We will verify your fix by measuring the execution time of the compiled `./anomaly_detector` on a large benchmark dataset (`/app/data/benchmark.log`). The verification suite will strictly evaluate the runtime metric. Ensure your fix is computationally efficient and terminates correctly.