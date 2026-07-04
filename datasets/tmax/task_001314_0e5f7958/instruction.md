You are a performance engineer profiling a new data processing application. The source code is located at `/home/user/processor.c`. It is intended to calculate the sum and variance of a large array of floating-point numbers concurrently using multiple threads.

However, the program is currently failing and producing incorrect results. It has three distinct issues:
1. **Core Dump/Segfault**: The program crashes with a segmentation fault when dividing work among threads.
2. **Race Condition**: The threads update shared variables unsafely, leading to non-deterministic and incorrect results across different runs.
3. **Precision Loss**: The program suffers from precision loss when accumulating the sum of a large array of floating-point numbers, leading to an inaccurate final sum.

Your task is to debug and fix the C code in `/home/user/processor.c` so that it computes the correct sum and variance without crashing, race conditions, or precision loss.

Requirements for the fix:
1. Resolve the out-of-bounds array access causing the segfault.
2. Fix the race condition. You may use mutexes, atomics, or thread-local accumulations that are aggregated at the end.
3. Change the accumulation variables and math logic to use `double` precision to prevent floating-point precision loss. Keep the initial array data as `float`.
4. The output format of the `printf` statements must remain exactly the same (printing to 5 decimal places: `Sum: %.5f` and `Variance: %.5f`), but you must update the format specifiers and variable types to handle `double`.

Once you have fixed the code:
1. Compile your program to `/home/user/processor` using the command: `gcc -O2 -pthread /home/user/processor.c -o /home/user/processor`
2. Run the program with exactly `10000000` (10 million) elements and `4` threads.
3. Save the standard output of this run to `/home/user/result.txt`.

Ensure the final results in `/home/user/result.txt` are deterministic and mathematically accurate.