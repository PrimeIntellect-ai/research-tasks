You are an on-call systems engineer responding to a 3:00 AM PagerDuty alert. 

The background telemetry processor is intermittently crashing and occasionally producing `NaN` (Not a Number) values for sensor reading standard deviations. 

The source code for the processor is located at `/home/user/processor.cpp`.
There is a directory of 1000 incoming telemetry files at `/home/user/data/` named `data_0.txt` through `data_999.txt`.

Each file contains lines of sensor data in the format: `timestamp,value`.

Your task:
1. Identify the intermittent failures: Find the specific files in the `/home/user/data/` directory that are causing the processor to crash or output `NaN`.
2. Fix the format parsing edge-case: The parser in `processor.cpp` uses a naive string split and conversion. It occasionally crashes on badly formatted lines (e.g., lines with a trailing comma and missing value like `1623456789,`). Modify the code to safely skip any lines that cannot be parsed as a valid double.
3. Fix the numerical instability: The processor calculates standard deviation using the naive sum-of-squares method. For sensor values that are very large but have very small variance, floating-point catastrophic cancellation results in a negative variance, causing `sqrt()` to return `NaN`. Replace this with a numerically stable algorithm (e.g., Welford's algorithm).
4. Recompile the program: `g++ -std=c++11 /home/user/processor.cpp -o /home/user/processor`
5. Process all data: Run your fixed `/home/user/processor` on all 1000 files in the `/home/user/data/` directory. 
6. Save the output: Write the standard output of the processor for all 1000 files into `/home/user/results.csv`. The format should exactly match the program's `cout` format: `filename,stddev`.

Ensure your fixed program does not output `NaN` and gracefully skips malformed lines without throwing exceptions.