Hello! We have a critical forensics issue. We are trying to reconstruct the timeline of a security breach across three of our microservices. Unfortunately, the microservices suffered from severe clock drift. 

To fix this, our team created a Go package called `logsync` to adjust the timestamps. The source code for this package has been vendored on the server at `/app/vendor/github.com/acmecorp/logsync`. However, it's not working correctly. The reconstructed logs are still out of order.

Here is what I need you to do:

1. **Fix the Formula Implementation**: Investigate the `logsync` package at `/app/vendor/github.com/acmecorp/logsync/sync.go`. There is a logic error in the `AdjustTimestamp(raw int64, drift float64) int64` function. The current implementation incorrectly applies the drift factor as a static millisecond offset. The correct formula should be: `adjusted = raw + int64(float64(raw) * drift)`. Please fix this package directly.

2. **Write the Log Reconstructor**: Create a Go program at `/home/user/log_reconstructor.go` and compile it to `/home/user/log_reconstructor`.
   - Your program must read a stream of log entries from `stdin`, one per line.
   - The input format for each line is: `SERVICE_ID|RAW_TIMESTAMP|DRIFT_FACTOR|MESSAGE`
     - Example: `SVC-A|1620000000|0.00015|User authentication failed`
   - **Assertion-based Validation**: Before processing, your program must validate each line. You must silently DROP (ignore) any line where:
     - `RAW_TIMESTAMP` is less than or equal to `0`.
     - `DRIFT_FACTOR` is strictly less than `-0.5` or strictly greater than `0.5`.
     - The line is malformed (does not have exactly 4 pipe-separated fields).
   - For all valid lines, use the fixed `logsync.AdjustTimestamp` function to calculate the corrected timestamp.
   - You must initialize your own go module in `/home/user/` and use a `replace` directive in your `go.mod` to point `github.com/acmecorp/logsync` to `/app/vendor/github.com/acmecorp/logsync`.

3. **Reconstruct the Timeline**: 
   - After reading `EOF` from `stdin`, your program must sort all the valid log entries by their *corrected* timestamp in ascending order.
   - If two entries have the exact same corrected timestamp, sort them alphabetically by `SERVICE_ID`.
   - If they are still equal, preserve their original relative input order (use a stable sort).

4. **Output Format**:
   - Print the sorted logs to `stdout`, one per line, in the exact following format:
     `[CORRECTED_TIMESTAMP] SERVICE_ID: MESSAGE`
     - Example: `[1620243000] SVC-A: User authentication failed`

I have a compiled reference binary from before the incident. I will be feeding both your `/home/user/log_reconstructor` and the reference binary thousands of random log lines to ensure your output is bit-exact equivalent. 

Please proceed and let me know when `/home/user/log_reconstructor` is built and ready!