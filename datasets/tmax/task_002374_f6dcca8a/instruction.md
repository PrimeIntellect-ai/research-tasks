You are a bioinformatics analyst tasked with modeling the population dynamics of a wild-type (WT) and mutant (MUT) bacterial strain. You have time-series data measuring the concentration of a byproduct, but the mutant data contains collinear features that cause standard matrix-based regression to fail. 

You must write a Go program at `/home/user/analyze.go` to solve this end-to-end.

**Background:**
The byproduct concentration $y(t)$ is modeled by the linearized ODE solution:
$y(t) = \theta_1 x_1(t) + \theta_2 x_2(t)$
where $x_1(t)$ and $x_2(t)$ are time-dependent biochemical features provided in the datasets.

For both WT and MUT strains, you need to estimate the parameters $\theta = [\theta_1, \theta_2]^T$ using ordinary least squares (OLS) via the normal equations: $\theta = (X^T X)^{-1} X^T Y$.

However, for the MUT strain, $x_1(t)$ and $x_2(t)$ are nearly identical (collinear) due to a pathway collapse, making $X^T X$ near-singular. A naive matrix inversion will fail or produce wild numerical instability.

**Your Tasks:**
1. **Regularized Curve Fitting:** 
   Write a Go program (using `math` and standard libraries, or you may `go get` a matrix library like `gonum.org/v1/gonum/mat`) to fit the parameters $\theta$ for both the WT and MUT datasets. 
   To handle the near-singular matrix in MUT, implement Ridge Regression (Tikhonov regularization) for *both* datasets:
   $\theta = (X^T X + \lambda I)^{-1} X^T Y$
   Use a regularization parameter $\lambda = 0.05$.

2. **ODE Forward Simulation:**
   Using the fitted parameters $\theta_{MUT}$, simulate the rate of change $dy/dt$ at $t=10$ using the simple ODE model: 
   $dy/dt = -0.1 \cdot y(t) + \theta_1 \cdot x_1(t) + \theta_2 \cdot x_2(t)$.
   Compute $y(10)$ first, then evaluate $dy/dt$.

3. **Statistical Hypothesis Comparison:**
   For the WT dataset, compare two hypotheses:
   - **H0 (Null):** $\theta_2 = 0$ (Reduced model, only fit $\theta_1$ using $\theta_1 = (X_1^T X_1 + \lambda)^{-1} X_1^T Y$, $\lambda=0.05$).
   - **H1 (Alternative):** $\theta_2 \neq 0$ (Full model with $\theta_1$ and $\theta_2$, fitted via Ridge as above).
   
   Calculate the Sum of Squared Errors (SSE) for both models: $SSE = \sum (y_i - \hat{y}_i)^2$.
   Compute the F-statistic:
   $F = \frac{(SSE_{H0} - SSE_{H1}) / 1}{SSE_{H1} / (N - 2)}$
   where $N$ is the number of data points.

**Input Data:**
The data files are located at `/home/user/wt_data.csv` and `/home/user/mut_data.csv`.
They contain headers: `t,x1,x2,y`.

**Output:**
Your Go program should write a JSON file to `/home/user/results.json` with the following structure:
```json
{
  "wt_theta1": 1.2345,
  "wt_theta2": 1.2345,
  "mut_theta1": 1.2345,
  "mut_theta2": 1.2345,
  "mut_dy_dt_at_10": 1.2345,
  "wt_f_statistic": 1.2345
}
```
*Round all JSON float values to 4 decimal places.*

Execute your Go script to generate the `results.json` file. Ensure the file is properly formatted.