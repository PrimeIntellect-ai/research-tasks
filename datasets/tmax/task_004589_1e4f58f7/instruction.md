You are a performance engineer profiling a mathematical solver backend. We are evaluating the stability and performance profile of a non-linear equation solver under specific workloads.

Your task is to analyze a dataset of constant values, compute roots using a specific numerical method, test for numerical stability, and compare the execution profiles (iteration counts) using a probability distribution distance metric. 

You can use any programming language you prefer to write your scripts.

**Step 1: Non-linear Equation Solving**
A list of 50 constant values ($C$) is provided in `/home/user/inputs.txt` (one per line). 
For each $C$, you must find a real root for the equation:
$f(x) = x^3 - 3x - C = 0$
Use Newton's Method with the following strict parameters:
- Initial guess $x_0 = 3.0$
- Convergence criterion: $|f(x_n)| \le 10^{-6}$
- Maximum iterations: 100
Record the root found and the number of iterations required. If it does not converge within 100 iterations, record the iteration count as 100 and the root as the value at iteration 100.

**Step 2: Numerical Stability Testing**
To test for numerical stability, repeat Step 1 for a perturbed set of constants. For each original $C$, compute $C' = C + 10^{-4}$. 
Find the new root using the exact same Newton's Method parameters.
An input $C$ is classified as **"unstable"** if the absolute difference between the root found for $C$ and the root found for $C'$ is strictly greater than $10^{-2}$.

**Step 3: Probability Distribution Distance**
We need to measure how the input perturbation shifts the performance profile.
Calculate the empirical probability mass function (PMF) of the *iteration counts* for the original $C$ values. Do the same for the perturbed $C'$ values.
Compute the Total Variation Distance (TVD) between these two discrete probability distributions. 
*Note: TVD between two probability distributions $P$ and $Q$ on a countable space is defined as $\frac{1}{2} \sum_{k} |P(k) - Q(k)|$.*

**Step 4: Regression Report**
Create a summary report at `/home/user/profiling_report.txt` containing exactly three lines:
Line 1: The total number of "unstable" inputs.
Line 2: The TVD between the original and perturbed iteration count distributions, rounded to exactly 4 decimal places (e.g., 0.1250).
Line 3: The maximum number of iterations required by any original $C$ value.

Make sure your output format strictly matches these requirements so the automated regression suite can verify it.