I am a performance engineer profiling a new parallel algorithm. I have a C source file located at `/home/user/profiler.c` that tests our application's scaling using OpenMP. 

Your task is to automate the compilation, execution, and statistical analysis of this performance profiler using entirely Bash.

1. **Compilation**: Compile `/home/user/profiler.c` into an executable named `/home/user/profiler`. Ensure you include the correct GCC flags to enable OpenMP support.
2. **Execution & Array Manipulation**: The compiled `/home/user/profiler` takes one integer argument: the number of trials. Write a Bash script at `/home/user/evaluate.sh` that runs `/home/user/profiler 5` to perform 5 trials. The profiler will output a 2D matrix (4 rows by 5 columns) of execution times in seconds. The rows correspond to thread counts of 1, 2, 4, and 8, respectively. 
3. **Statistical Analysis**: In your `evaluate.sh` script, parse this 2D text output using Bash. Calculate the mean execution time for 1 thread (Row 1) and 8 threads (Row 4). You must use `bc` or standard bash tools for floating-point arithmetic.
4. **Hypothesis Testing**: Calculate the parallel speedup (Mean Time 1-Thread / Mean Time 8-Thread). Evaluate the statistical hypothesis: "Is the parallel speedup strictly greater than 4.00?".
5. **Reporting**: Your script must generate a report at `/home/user/summary.log` with exactly the following format (rounding floats to two decimal places):

```
Mean 1-thread: <value>
Mean 8-thread: <value>
Speedup: <value>
Hypothesis Met: <YES/NO>
```

Run your `/home/user/evaluate.sh` script so that `/home/user/summary.log` is generated.