You are assisting a statistical researcher in running a Monte Carlo simulation based on observational data. 

The researcher has provided a raw data file at `/home/user/raw_data.txt`. This file contains 4 columns of space-separated values: `Timestamp`, `SensorA`, `SensorB`, and `SensorC`.

Your objectives are:
1. **Observational Data Reshaping:** Read `/home/user/raw_data.txt`, drop the `Timestamp` column, and write the remaining three columns to a new comma-separated file at `/home/user/processed.csv`. The output file should not have a header row.
2. **Scientific Software Compilation & Debugging:** The researcher has provided a Go simulation tool located in `/home/user/sim/`. The tool reads the CSV, computes the covariance matrix of the sensors, and attempts to generate multivariate normal samples using Cholesky factorization. However, because `SensorC` is a linear combination of `SensorA` and `SensorB`, the covariance matrix is singular, and the matrix factorization fails with an error. 
   - You must fix the Go code (`/home/user/sim/main.go`) by adding a ridge penalty (jitter) of exactly `1e-3` (0.001) to the diagonal elements of the covariance matrix right before the Cholesky factorization is performed.
   - Initialize the module and compile the tool (you may use `gonum.org/v1/gonum/mat` and `stat` which the code relies on). Name the compiled binary `sim_tool`.
3. **Convergence Testing:** The compiled `sim_tool` accepts a flag `-n` specifying the number of Monte Carlo samples to draw, and it prints the estimated mean of `SensorC` to standard output. 
   - The theoretical mean of `SensorC` based on the raw data is exactly `5.5`.
   - Write a script to test values of `n` starting from `1000`, incrementing by `1000` (i.e., 1000, 2000, 3000...). 
   - Find the *smallest* `n` where the absolute difference between the simulated mean of `SensorC` and the theoretical mean (5.5) is strictly less than `0.02`.

Once you have found this minimum `n`, create a file at `/home/user/convergence_result.txt` containing only the integer value of this `n`.