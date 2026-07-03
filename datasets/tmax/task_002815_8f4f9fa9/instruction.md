You are a researcher conducting a convergence study on a domain decomposition method. 

In the directory `/home/user/task`, you will find:
- `partial_<N>_<i>.dat`: Pre-computed partial simulation files for different levels of mesh refinement (`N` = 2, 4, 8, 16 subdomains). Each file contains a 1D array of floats.
- `reference.dat`: The true, analytical probability distribution.
- `compute_distance.py`: A Python script that calculates the L2 distance between two data files (usage: `python3 compute_distance.py file1.dat file2.dat`).
- `aggregate.sh`: A Bash script that takes `N` (number of subdomains) as an argument and sums the corresponding partial files element-wise to produce `result_<N>.dat`.

Currently, `aggregate.sh` uses `find` to gather the partial files and pipes them to `awk` for summation. However, `find` returns files in a non-deterministic order. Due to the properties of floating-point arithmetic (reduction order), this non-deterministic processing order leads to slight, non-reproducible variations in the final sum.

Your objectives:
1. **Fix Reproducibility**: Modify `/home/user/task/aggregate.sh` so that it passes the partial files to `awk` in **strictly increasing numerical order** of their subdomain index `i` (i.e., `partial_${N}_1.dat`, `partial_${N}_2.dat`, ..., `partial_${N}_N.dat`). Do not change the underlying mathematical operation in the `awk` command, only the file input order.
2. **Execute Aggregation**: Run your fixed `aggregate.sh` for each refinement level: `N = 2, 4, 8, 16`.
3. **Convergence Testing**: For each `N`, compute the L2 distance between the newly generated `result_<N>.dat` and `reference.dat` using `compute_distance.py`.
4. **Log Results**: Create a log file at `/home/user/task/convergence.log`. Write the distance for each `N` on a new line, formatted exactly as:
   `N=<N> distance=<distance>`
   Sort the log file by `N` in ascending numerical order (2, 4, 8, 16).

Ensure all scripts are run from within `/home/user/task` and that the final log file is exactly at `/home/user/task/convergence.log`.