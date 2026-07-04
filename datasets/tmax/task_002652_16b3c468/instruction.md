You are an AI assistant helping a data scientist fit a nonlinear dynamical model to experimental time-series data. 

We are studying a sequential chemical reaction $A \rightarrow B \rightarrow C$ with nonlinear kinetics. The system of Ordinary Differential Equations (ODEs) is:

$dA/dt = -k_1 A$
$dB/dt = k_1 A - k_2 B^2$
$dC/dt = k_2 B^2 - k_3 C$

You are provided with experimental data in a CSV file located at `/home/user/kinetics_data.csv`. The file has columns `t, A, B, C`. The initial conditions at $t=0$ are exactly the values in the first row of this dataset.

Your task is to:
1. **Parallel Grid Search:** We need to find the best parameters $(k_1, k_2, k_3)$ that minimize the Sum of Squared Errors (SSE) between the simulated model trajectories and the experimental data across all three chemical species ($A, B, C$). 
   Search the following parameter space:
   - $k_1 \in [0.1, 1.0]$ with 10 evenly spaced values (0.1, 0.2, ..., 1.0)
   - $k_2 \in [0.1, 1.0]$ with 10 evenly spaced values (0.1, 0.2, ..., 1.0)
   - $k_3 \in [0.1, 1.0]$ with 10 evenly spaced values (0.1, 0.2, ..., 1.0)
   This creates exactly 1,000 parameter combinations. You **must** parallelize the evaluation of these 1,000 combinations using at least 4 parallel processes/workers to speed up the computation.
   
2. **Matrix Decomposition:** Once you identify the best parameter set $(k_1, k_2, k_3)$ that yields the lowest SSE, simulate the system using these best parameters. Extract the simulated trajectory matrix $M$ of size $N \times 3$ (where $N$ is the number of time points, and columns are the simulated values of $A, B, C$). Perform Singular Value Decomposition (SVD) on matrix $M$ and extract the largest singular value ($\sigma_1$).

3. **Output:** Create a JSON file at `/home/user/best_fit.json` with the following structure. All numerical values must be floats rounded to exactly 4 decimal places.
```json
{
  "best_k1": 0.0000,
  "best_k2": 0.0000,
  "best_k3": 0.0000,
  "sse": 0.0000,
  "sigma_1": 0.0000
}
```

You can use any programming language (e.g., Python, R, Julia) available or installable in your terminal environment to complete this task. Write your scripts, run them, and ensure `/home/user/best_fit.json` is generated exactly as specified.