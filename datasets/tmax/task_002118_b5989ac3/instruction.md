You are a performance engineer tasked with analyzing memory allocation telemetry from a distributed cluster. The raw telemetry has been extracted into a CSV file, and you need to determine how closely its primary variance component matches a baseline distribution using Go.

You have been provided with two files:
1. `/home/user/telemetry.csv`: A matrix of observational data where rows represent time-steps and columns represent cluster nodes.
2. `/home/user/baseline.csv`: A single row of comma-separated values representing the reference probability distribution of memory allocations across the nodes.

Your objective is to write and execute a Go program (`/home/user/analyze.go`) that does the following:
1. **Observational Data Reshaping**: Read `/home/user/telemetry.csv` and parse it into a floating-point matrix $A$.
2. **Matrix Decomposition**: Use the `gonum.org/v1/gonum/mat` library to perform Singular Value Decomposition (SVD) on matrix $A$. 
3. Extract the first right singular vector (the first column of $V$, where $A = U \Sigma V^T$). Let's call this vector $v$.
4. Transform $v$ into a probability distribution $P$:
   - Take the absolute value of each element in $v$.
   - Normalize the vector by dividing each element by the sum of all elements, so that the elements sum to 1.0.
5. **Probability Distribution Distance**: Read `/home/user/baseline.csv` to get the baseline distribution $Q$. Calculate the Kullback-Leibler (KL) divergence from $Q$ to $P$, defined as:
   $D_{KL}(P \parallel Q) = \sum_{i} P_i \ln\left(\frac{P_i}{Q_i}\right)$
   (Use the natural logarithm).
6. Save the final KL divergence value to `/home/user/kl_result.txt`, formatted to exactly 6 decimal places (e.g., `0.123456`).

Constraints & Setup:
- You must write the solution in Go. Initialize your module in `/home/user/analysis` (so your code will be `/home/user/analysis/analyze.go`).
- Ensure all dependencies are properly fetched.
- Execute your code to produce the final `kl_result.txt` file.