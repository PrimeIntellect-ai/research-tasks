You are an IT support technician acting on an escalated critical ticket. Our mathematical sensor aggregation pipeline is failing. Customers are reporting three distinct issues:

1. **Log Timeline Confusion:** We have three services outputting logs to `/home/user/logs/service1.log`, `/home/user/logs/service2.log`, and `/home/user/logs/service3.log`. An anomaly occurred, but the timestamps are interleaved and use different local formats.
2. **Inconsistent Math Results:** The core Go application at `/home/user/app/sensor_agg.go` computes the sum of squares for incoming data arrays. Sometimes it yields correct results; other times, the results are wildly incorrect under load.
3. **Serialization Errors:** When the Go application outputs the results, the JSON structure is malformed, specifically the `variance` field is being output as a hex string instead of a standard float, breaking downstream diff analysis tools.

**Your objectives:**

1. **Log Reconstruction:** Analyze the three log files in `/home/user/logs/`. Find the exact timestamp of the line containing the word `CRITICAL_ANOMALY`. Write *only* the unified ISO-8601 timestamp (e.g., `2023-10-25T14:32:01Z`) of that event into `/home/user/anomaly_time.txt`.
2. **Fix Concurrency:** Inspect `/home/user/app/sensor_agg.go`. Identify and fix the data race condition in the `ComputeSumOfSquares` function. You must ensure it continues to process the array concurrently but calculates the correct total without race conditions.
3. **Fix Serialization:** Identify the custom JSON marshaling bug in `/home/user/app/sensor_agg.go` that outputs the `variance` field incorrectly. Fix it so it outputs standard decimal floats.
4. **Process Data:** Build your fixed Go application (`go build -o app_bin sensor_agg.go`). Run it against `/home/user/data/input.json` and direct its standard output to `/home/user/output.json`.

Ensure your fixes in the Go code use standard library features. Do not change the function signatures or the core mathematical logic (sum of squares), just fix the race condition and the JSON encoding.