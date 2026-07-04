You are an automation specialist building a data processing pipeline for a dual-sensor tracking system. We have raw logs from two sensors, but they are unordered, contain some mismatched timestamps, and need to be processed efficiently. 

Your task is to create a workflow that aligns the data, computes the 3D Euclidean distance between the sensors at matching timestamps, filters out invalid anomalies, and does so using a combination of Bash scripting (for orchestration and parallelism) and C (for mathematical computations).

**Input Data:**
There are two space-separated log files located at:
- `/home/user/sensor1.txt`
- `/home/user/sensor2.txt`

Each file has the format: `<UnixTimestamp> <X> <Y> <Z>`

**Requirements:**
1. **Timestamp Alignment & Join:** Write a bash script `/home/user/process.sh` that first sorts both files by timestamp, and then joins them so that only records with exactly matching timestamps are kept. The joined format should be: `<Timestamp> <X1> <Y1> <Z1> <X2> <Y2> <Z2>`.
2. **Distance Computation & Validation (C Program):** Write a C program at `/home/user/distance.c` that reads this joined data from standard input. For each line, compute the 3D Euclidean distance between the two points `(X1, Y1, Z1)` and `(X2, Y2, Z2)`. 
   - **Validation Gate:** Only output the result if the computed distance is less than or equal to `10.00`.
   - The output should be printed to standard output in the format: `<Timestamp> <Distance>`, with the distance formatted to exactly two decimal places.
3. **Parallel Processing:** In your `/home/user/process.sh` script, after joining the files, split the joined data into chunks of 100 lines. Process these chunks in parallel through your compiled C program (using `xargs -P` or background jobs) to maximize throughput.
4. **Final Output:** The final output from the parallel processing must be concatenated and sorted by timestamp, then saved to `/home/user/valid_distances.txt`.

**Execution:**
- Compile your C program to `/home/user/distance_calc` (remember to link the math library).
- Ensure `/home/user/process.sh` is executable.
- Run `/home/user/process.sh` to generate the final output at `/home/user/valid_distances.txt`.