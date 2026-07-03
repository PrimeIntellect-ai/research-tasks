You are an operations engineer triaging an incident involving a mathematical pipeline that analyzes sensor data. The pipeline consists of a SQLite database and a high-performance C program that calculates the sample variance of the sensor readings.

The pipeline recently crashed and left the system in a broken state. You need to investigate and fix the issues:

1. **Database Recovery**: The database was corrupted and dumped to an incomplete/malformed SQL recovery file at `/home/user/pipeline/recovery.sql`. The final few lines contain syntax errors caused by the crash. Fix the SQL file and restore it into a new SQLite database at `/home/user/pipeline/sensor.db`.

2. **Build Failure Diagnosis**: The C program used for calculations is located at `/home/user/pipeline/variance.c`. However, running `make` in `/home/user/pipeline/` currently fails. Diagnose and fix the build issue so that the `variance` executable compiles successfully.

3. **Floating-point Precision Repair**: The C program implements a naive variance calculation. Because the sensor readings have a large constant offset (e.g., ~1,000,000) but tiny variations, the current algorithm suffers from catastrophic cancellation, resulting in an output of `0.000000` or wildly incorrect numbers. Modify `/home/user/pipeline/variance.c` to use a numerically stable algorithm (like a two-pass mean or Welford's algorithm) to correctly compute the sample variance. The program reads floating-point numbers from standard input (one per line) and should print only the final variance to standard output, formatted to 6 decimal places (e.g., `printf("%.6f\n", var)`).

4. **Regression Test Construction**: Write a bash or Python script at `/home/user/pipeline/test_variance.sh` (or `.py`) that:
   - Queries all the `value`s from the `readings` table in `/home/user/pipeline/sensor.db`.
   - Passes them via standard input to the compiled `./variance` executable.
   - Verifies that the program outputs the correct variance. If the output is correct, exit with code 0; otherwise, exit with code 1.

5. **Final Output**: Run your corrected C program on the recovered database values and save the exact output (just the number, to 6 decimal places) into `/home/user/pipeline/final_result.txt`.

Ensure all files are created exactly at the specified paths. The `/home/user/pipeline` directory already exists and contains the initial files.