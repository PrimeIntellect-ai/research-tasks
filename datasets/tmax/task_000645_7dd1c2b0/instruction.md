You are the on-call engineer, and you've just been paged at 3:00 AM. The primary data synchronization service (`sensor_service`) has stopped working. It processes sensor telemetry but is currently failing in three distinct ways:

1. **Occasional Crashes (Segfaults):** There is a specific payload in the large `/home/user/sensor_service/sensors.log` file that is causing the application to crash.
2. **Race Conditions:** The workers occasionally report incorrect metrics for corrupted packets due to thread-safety issues.
3. **Convergence/Timezone Failure:** A subtle timezone and encoding bug in the timestamp parser is causing the epoch time calculations to return `-1` or garbage values, causing the synchronization loop to fail to converge on the correct time offset.

Your tasks are:
1. **Delta Debugging / Test Minimization:** Analyze `/home/user/sensor_service/sensors.log` to find the exact single line that triggers the segmentation fault. Save this exact single line to `/home/user/minimal_crash.log`.
2. **Fix the C Code:** Modify `/home/user/sensor_service/worker.c` to:
   - Eliminate the race condition affecting the `corrupted_packets` global variable.
   - Fix the timestamp parsing logic in the `parse_timestamp` function. The function currently leaves fields of `struct tm` uninitialized before calling `mktime()`, which causes erratic behavior and timezone/DST shifts. Fix it so that the structure is properly zero-initialized and DST is properly handled or ignored (e.g., setting `tm_isdst = -1`).
   - Fix the crashing logic so it skips the crashing payload gracefully instead of segfaulting.
3. **Build and Run:** 
   - Compile the fixed code using the existing `Makefile` in `/home/user/sensor_service/`.
   - Run the compiled `sensor_sync` binary with `sensors.log` as the argument.
   - Redirect the standard output of the successful run to `/home/user/success.out`.

The final state must have the corrected `worker.c`, the compiled binary, `/home/user/minimal_crash.log` containing exactly one line, and `/home/user/success.out` containing the successful execution summary.