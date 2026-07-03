You have just joined a new team and inherited an unfamiliar C codebase located in `/home/user/clustering`. The code implements a custom K-Means-like 1D clustering algorithm for a specialized data pipeline. 

The system operates by piping binary floating-point data into the clustering program. However, the CI system reports that the program intermittently fails to converge, eventually outputting `NaN` for cluster centroids or crashing entirely. 

Your task is to:
1. Investigate the codebase in `/home/user/clustering`.
2. Reproduce the intermittent failures by running the provided `/home/user/run_tests.sh` script.
3. Use debugging techniques (e.g., system call tracing, adding intermediate state assertions) to identify the root causes. There are two primary bugs:
   - A system-level I/O bug causing intermittent data loss when reading from standard input.
   - An algorithmic bug causing a convergence failure (division by zero) when a cluster becomes empty.
4. Modify `cluster.c` to fix both issues.
   - Ensure the standard input reading mechanism is robust against partial reads.
   - Add proper assertion-based validation and fix the algorithm so that empty clusters do not cause `NaN` propagation (if a cluster's count is 0, its centroid should remain unchanged).
5. Compile the fixed code into an executable named `cluster_fixed` in `/home/user/clustering`.
6. Run `/home/user/run_tests.sh` again to ensure it passes 100% of the time. 
7. Once fixed, run the program one final time using the command `cat /home/user/clustering/data.bin | ./cluster_fixed > /home/user/final_output.txt`.

Ensure `/home/user/final_output.txt` contains the final valid centroids, formatted exactly as output by the provided `print_centroids` function.