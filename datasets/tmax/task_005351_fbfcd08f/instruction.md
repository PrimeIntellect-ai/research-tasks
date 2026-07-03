You are a performance engineer profiling a scientific application. You have been provided with a C program located at `/home/user/compute_jsd.c`. This program calculates the Jensen-Shannon Divergence (JSD), a probability distribution distance metric, between two unnormalized probability density functions using numerical integration (the trapezoidal rule).

Currently, the program runs sequentially and takes too long to execute for large grid sizes. 

Your tasks are to:
1. Modify `/home/user/compute_jsd.c` to parallelize the two main numerical integration loops using OpenMP. Use the appropriate OpenMP pragmas for parallelizing `for` loops with reduction variables.
2. Compile the modified code into an executable at `/home/user/compute_jsd`. You must use `gcc` with the `-O3` optimization flag, the `-lm` flag for the math library, and the flag required to enable OpenMP.
3. Run the compiled executable and redirect its standard output (a single floating-point number representing the JSD) to `/home/user/jsd_output.txt`.
4. Create a bash profiling script at `/home/user/profile.sh` that measures the execution time of the `./compute_jsd` executable. The script must:
   - Run the executable exactly 3 times sequentially.
   - Use the system `time` command (`/usr/bin/time -f "%e" ./compute_jsd`) to capture the elapsed real time in seconds for each run.
   - Append the elapsed time of each run (just the numerical value) to a file named `/home/user/times.txt`.
   - Discard the standard output of `./compute_jsd` during these profile runs so only the times are captured in `times.txt`.
5. Ensure `/home/user/profile.sh` is executable and run it to generate the `/home/user/times.txt` file.

Do not change the mathematical logic or the grid size in the C program; only add the necessary OpenMP pragmas.