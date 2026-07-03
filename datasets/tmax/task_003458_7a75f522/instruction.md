You are a support engineer acting as a forensics investigator for a client's telemetry aggregation system. The client has provided you with a Rust application located at `/home/user/telemetry_app` and a raw data dump located at `/home/user/telemetry_app/data/sensors.log`. 

The client reported two major issues:
1. **Application Crashes:** The application frequently crashes with a panic when processing production logs. You need to analyze the traceback/logs to figure out why.
2. **Inaccurate Aggregations:** Even when the client manually removed the lines causing crashes, they noticed that the computed average is highly inaccurate due to floating-point precision loss when accumulating a mix of extremely large and very small sensor readings.

Your tasks are to:
1. Debug and modify the Rust application in `/home/user/telemetry_app` so that it handles parsing edge-cases gracefully. Specifically, if a sensor value cannot be parsed as a valid floating-point number (e.g., corrupted data like "ERR" or malformed floats), the program should simply skip that line rather than crashing.
2. Repair the floating-point precision issue. The accumulator currently loses precision. Upgrade the math logic to use 64-bit precision (`f64`) for summing and calculating the average.
3. Build and run the fixed application against `/home/user/telemetry_app/data/sensors.log`.
4. Capture the final output of the program (which prints `Average: <value>`) and save it exactly as it is outputted to a new file at `/home/user/diagnostics.txt`.

Ensure the final average is computed accurately using `f64` types and properly skips invalid format lines.