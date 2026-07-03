You are a performance engineer responsible for profiling and maintaining a legacy sensor processing application. You've been tasked with analyzing a program that processes a large dataset of sensor readings, but the pipeline is currently failing.

The application source code is located at `/home/user/sim_profiling/simulation.c` and the dataset is at `/home/user/sim_profiling/sensor_data.txt`.

Currently, the application has two major issues:
1. **Corrupted Input Handling**: The program hangs or crashes in an infinite loop when it encounters malformed (non-numeric) data in the `sensor_data.txt` file. You must analyze the application's execution, identify where it fails, and modify `simulation.c` to gracefully skip over corrupted lines (any line that cannot be parsed as a float) and continue processing the rest of the file.
2. **Floating-point Precision**: Even if the program runs to completion, the final accumulated sum is inaccurate due to catastrophic precision loss when accumulating many small floating-point values into a single-precision `float`. You must repair this by upgrading the accumulation logic to use double precision (`double`). 

Your tasks are to:
1. Debug and modify `/home/user/sim_profiling/simulation.c` to fix both the input handling and the floating-point precision issues.
2. Ensure the final `printf` outputs the total sum using the format `"Total Sum: %.4f\n"`.
3. Compile your fixed code into an executable named `/home/user/sim_profiling/sim_fixed`. (Use standard `gcc`).
4. Run the executable and redirect its standard output to `/home/user/sim_profiling/final_result.txt`.

The automated test will verify the presence and correct contents of `/home/user/sim_profiling/final_result.txt`, as well as inspect the modified source code.