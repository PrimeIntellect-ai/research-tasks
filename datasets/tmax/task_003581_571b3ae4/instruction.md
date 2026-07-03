As a performance engineer, you are investigating an application's resource usage anomalies. We have recorded a visualization of the CPU load over time in a video file located at `/app/profile_viz.mp4`. 

Your task consists of two parts:

**Part 1: Data Extraction**
1. The video `/app/profile_viz.mp4` displays a sequence of frames. Exactly once per second (at 00:00:01, 00:00:02, etc.), the video flashes a solid grayscale color that represents the CPU load. 
2. Use `ffmpeg` and basic CLI tools to extract the average grayscale intensity (0-255) for the frame at each exact second mark.
3. Save these integer values, one per line, into `/home/user/extracted_loads.txt`.

**Part 2: Statistical Optimization Script**
Write a pure Bash script (using only shell builtins, `awk`, or `bc`) at `/home/user/optimizer.sh` that implements a discrete genetic optimization and convergence test. The script must take exactly one argument: a comma-separated string of integer baseline loads (e.g., `45,120,60,200`).

The script must perform the following algorithm and output a single integer representing the "optimized load threshold":
1. Initialize a population of 3 candidate thresholds: `T1 = min(loads)`, `T2 = max(loads)`, `T3 = floor(average(loads))`.
2. For exactly 10 iterations:
   a. Calculate the "fitness" of each candidate `T`: Fitness is the sum of absolute differences between `T` and all load values in the input string. Lower fitness is better.
   b. Find the candidate with the lowest fitness (the "best" candidate). If there is a tie, pick the one with the lowest `T` value.
   c. Generate two new candidates (mutations) from the best candidate: `New_T1 = best_T - 5` and `New_T2 = best_T + 5`.
   d. The new population for the next iteration becomes: `best_T`, `New_T1`, and `New_T2`.
3. After 10 iterations, output the `best_T` value from the final population to standard output (just the integer, followed by a newline).

Your script must be robust, executable (`chmod +x /home/user/optimizer.sh`), and must exactly implement the logic above. We will verify your script by fuzzing it with thousands of random input lists and comparing its output bit-for-bit against our reference implementation.

Please complete Part 1 and Part 2.