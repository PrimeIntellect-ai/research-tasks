You are an engineer investigating issues in a long-running sensor data processing service written in C. 
The service has been experiencing multiple issues:
1. It crashes occasionally due to a buffer overflow when receiving specific malicious sensor names. A memory dump of the crash is available at `/home/user/crash_dump.bin`.
2. The aggregated total sum of sensor readings is incorrect (lower than expected).
3. Memory usage grows continuously over time (memory leak).

Your tasks are:
1. Analyze the memory dump `/home/user/crash_dump.bin` to find the long, malicious sensor name that caused the crash. The malicious name starts with `SENSOR_OVERFLOW_` and is followed by a trigger sequence.
2. Fix the source code located at `/home/user/sensor_service.c`. You must:
   - Fix the buffer overflow vulnerability in `process_data`.
   - Fix the memory leak.
   - Fix the race condition preventing the total sum from calculating correctly across multiple threads.
   - Fix the floating-point precision accumulation issue (the total sum must be completely accurate, without precision loss from adding millions of tiny values).
3. Compile and run your fixed version of `sensor_service.c`.
4. Create a file `/home/user/solution.txt` with exactly two lines:
   - Line 1: The malicious sensor name extracted from the crash dump.
   - Line 2: The exact output of the fixed `sensor_service` (the final correct total sum, formatted to 6 decimal places).

Do not change the loop counts or the value being added (`0.000001`). Only fix the bugs.