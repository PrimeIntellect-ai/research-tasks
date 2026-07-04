You are a performance engineer profiling a sensor data aggregation tool. 

You have been provided with a C program at `/home/user/sensor_stat.c` that calculates the standard deviation of an array of sensor readings passed as command-line arguments.

Currently, the pipeline has several issues:
1. The provided build script `/home/user/build.sh` fails to compile the program.
2. Even when compiled, the program suffers from catastrophic cancellation (a floating-point precision issue) when processing large sensor values with very small variances. This results in negative variances and consequently `NaN` when taking the square root.
3. We need to ensure the program is robust against these precision errors.

Your task:
1. Diagnose and fix the build failure in `/home/user/sensor_stat.c` and/or `/home/user/build.sh`.
2. Fix the floating-point precision repair in `/home/user/sensor_stat.c`. You must replace the single-pass variance algorithm with a numerically stable **two-pass algorithm** (compute the mean first, then compute the sum of squared differences from the mean) and use `double` precision variables instead of `float`.
3. Compile the fixed program to `/home/user/sensor_stat` using the fixed `/home/user/build.sh`.
4. Run the provided fuzzing script `/home/user/fuzz.sh`, which will invoke your compiled program with 100 randomized high-magnitude, low-variance inputs.
5. The fuzz script will automatically generate a log at `/home/user/fuzz_results.log`. If your precision fix is correct, the script will write "PASS" to `/home/user/fuzz_status.txt`.

Ensure that `/home/user/fuzz_status.txt` contains exactly `PASS` as its final state.