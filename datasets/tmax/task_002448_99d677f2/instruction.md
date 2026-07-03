You are an operations engineer triaging a recent incident in our mathematical processing pipeline. The pipeline calculates the sum of squares of sensor readings.

The pipeline consists of two components written in different languages:
1. `encode.py` (Python): Simulates reading sensor data, standardizes it, and serializes the floating-point numbers to a binary file (`data.bin`).
2. `compute.c` (C): Reads the serialized binary file and calculates the sum of squares.

Recently, the automated pipeline tests started failing. The C program is outputting wildly incorrect results (often resulting in extremely large numbers or NaN) instead of the expected sum of squares.

The code is located in a Git repository at `/home/user/sensor_pipeline`. 
There is a test script provided at `/home/user/sensor_pipeline/test.sh` that compiles the C program, runs the Python encoder, runs the C compute engine, and checks if the result is correct.

Your tasks:
1. Use Git bisection to find the exact commit that introduced the regression. 
2. Analyze the intermediate state (`data.bin`) and the code in both languages to understand the encoding/serialization root cause.
3. Write the full 40-character SHA-1 hash of the first bad commit to the first line of the file `/home/user/bad_commit.txt`.
4. On the second line of `/home/user/bad_commit.txt`, write the expected file size (in bytes) of `data.bin` if the pipeline were functioning correctly without the serialization bug.

Do not push any changes or modify the Git history.