You are a performance engineer analyzing a new microservice. You suspect the response latency can be modeled as a linear combination of three system metrics: CPU utilization (%), Memory utilization (%), and I/O wait time (ms). 

The latency model is:
`Latency = (w_cpu * CPU) + (w_mem * Mem) + (w_io * IO)`

You have gathered a reference dataset of these metrics and the corresponding observed latencies in a CSV file located at `/home/user/perf_data.csv` (which is already created for you).

Your task has three parts:
1. **Optimization (C++)**: Write a C++ program in `/home/user/optimizer.cpp` that reads `/home/user/perf_data.csv` and uses an optimization algorithm (like Gradient Descent or Exact Least Squares) to determine the optimal weights (`w_cpu`, `w_mem`, `w_io`) that minimize the Mean Squared Error (MSE) against the reference dataset. The program should output these derived weights to a file named `/home/user/weights.txt` in the exact format: `CPU=X.XX MEM=Y.YY IO=Z.ZZ` (where X, Y, Z are the weights rounded to exactly two decimal places).
2. **Execution**: Compile the C++ program using `g++` and run it to produce `/home/user/weights.txt`.
3. **Visualization (Bash)**: Write a bash script named `/home/user/visualize.sh` that reads `/home/user/perf_data.csv` and your `/home/user/weights.txt`. For each row in the CSV, it should calculate the predicted latency using your weights, compare it to the actual latency, and print an ASCII bar chart of the actual latencies to standard output. For each row, print the Row ID, the predicted latency (rounded to 2 decimals), and a number of `*` characters equal to `floor(Actual_Latency / 10)`. 

For example, your bash script output should look like this:
```
Row 1: Pred=69.00 Actual: ******
Row 2: Pred=145.00 Actual: **************
...
```

Ensure the bash script is executable and functions correctly. All code should be written from scratch using standard libraries and standard bash utilities.