You are a support engineer investigating a severe issue in a telemetry processing service. We have a Go application that occasionally leaks goroutines and completely hangs when reading batch telemetry logs from disk. 

A customer has provided a crashing log file, `payload.bin`, which causes the service to hang indefinitely (or trigger our watchdog timeout). 

Your diagnostic task involves the following steps:

1. **Test Minimization (Delta Debugging):**
   The `payload.bin` file contains multiple 8-byte telemetry entries. Most of them are processed normally, but one specific 8-byte sequence is triggering a precision-loss edge case in our floating-point format parsing, leading to an infinite loop. 
   Isolate the exact 8-byte chunk that causes the failure. Write these 8 bytes as a continuous lowercase hex string (16 characters, no spaces) to `/home/user/minimal_hex.txt`.

2. **Root Cause Diagnosis and Repair:**
   Review the source code provided in `/home/user/service.go`. You will notice a decay calculation loop. The problematic telemetry value causes precision loss where subtracting a small step from a massive float64 value results in the exact same float64 value, causing the loop to never terminate. Additionally, the goroutine fails to respect the cancellation context.
   
   Modify `/home/user/service.go` to fix this issue. Your fix MUST:
   - Include a check for `ctx.Done()` inside the decay loop to prevent goroutine leaks when a timeout occurs.
   - Gracefully handle or break out of the loop if precision loss is detected (e.g., if the value does not decrease after subtraction).

3. **Verification:**
   Compile your fixed service to `/home/user/fixed_service`.
   ```bash
   go build -o /home/user/fixed_service /home/user/service.go
   ```
   When run against the original `/home/user/payload.bin`, `/home/user/fixed_service` must exit successfully (exit code 0) without triggering the watchdog timeout.

The environment has Go installed. All files are in `/home/user/`.