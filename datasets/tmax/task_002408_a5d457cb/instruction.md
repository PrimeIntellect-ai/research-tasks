You are an on-call engineer at a financial tech company. It is 3 AM, and you have just been paged because the Pricing Engine service has completely locked up. The API Gateway is returning 504 Timeouts for all new requests.

Your objectives:

1. **Log Timeline Reconstruction**:
   There are two log files located in `/home/user/logs/`:
   - `api-gateway.log`: Contains incoming requests with transaction IDs (`tx_id`) and the requested `rate` parameters.
   - `pricing-engine.log`: Contains the internal logs of the pricing engine.
   Due to a recent deployment, the clocks on the two servers drifted. You must correlate the logs to find the exact `tx_id` and the `rate` parameter that caused the Pricing Engine to crash/hang (the engine starts processing it but never finishes, causing subsequent requests to pile up).
   Create a file at `/home/user/bug_report.txt` containing exactly two lines:
   Line 1: The crashing `tx_id`
   Line 2: The crashing `rate` value

2. **Build Failure Diagnosis**:
   The source code for the pricing engine is located in `/home/user/pricing-engine/`. The previous engineer tried to push a quick patch but broke the build. You need to fix the build issues. The project should build successfully using standard `go build`.

3. **Precision Loss & Loop Termination**:
   The pricing algorithm in `/home/user/pricing-engine/main.go` uses the Newton-Raphson method to calculate a specific financial yield. However, for the specific crashing `rate` you identified, the engine enters an infinite loop. This is due to a precision loss issue combined with a strict loop termination condition.
   - Debug and fix the precision loss issue (hint: consider the floating-point types being used).
   - Fix the loop termination so that it safely converges without infinite looping.

4. **Service Restoration**:
   Once the code is fixed and built, start the service so it listens on port 8080.
   Write a shell script at `/home/user/run.sh` that compiles the Go code and starts the binary in the background.

Ensure that the fixed service can successfully process the crashing `rate` via a GET request to `http://localhost:8080/calculate?rate=<CRASHING_RATE>`.