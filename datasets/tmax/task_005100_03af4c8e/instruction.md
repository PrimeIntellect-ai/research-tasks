You are an IT support technician responding to an escalated ticket. 

**Ticket #4491:**
"Our daily batch processor `calc_engine` is crashing with a Segmentation Fault when processing today's data file. It looks like a math issue causing a memory error, but the logs are completely useless. Please diagnose the crash, fix the source code, and run the program to generate the required output."

**Environment:**
- Source code: `/home/user/calc_engine.cpp`
- Input data: `/home/user/input_batch.dat`

**Your objective:**
1. Analyze the crash. You may compile the code with debug symbols and use tools like `gdb` or `strace` to trace the execution and identify the root cause.
2. You will find that a numerical instability (division by zero or near-zero catastrophic cancellation) results in an `Inf` or `NaN` value, which is then incorrectly cast to an integer and used as an array index, causing the segfault.
3. Fix the C++ code in `/home/user/calc_engine.cpp`. If the absolute difference between `x` and `y` is exactly zero, set the `metric` to `0.0` and the `index` to `0` to safely avoid the crash.
4. Compile your fixed code into an executable named `/home/user/calc_engine`.
5. Run the executable. It must read `/home/user/input_batch.dat` and successfully write all results to `/home/user/output.txt`.

Ensure the final compiled binary is at `/home/user/calc_engine` and the output file is at `/home/user/output.txt`.