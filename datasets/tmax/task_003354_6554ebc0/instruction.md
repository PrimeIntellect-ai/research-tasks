You are acting as a computational assistant for a researcher running statistical physics simulations. We need to determine the steady-state parameter of a system, generate its theoretical probability distribution, and compare it against empirical observations. 

You are provided with an empirical distribution in `/home/user/empirical.csv` which contains two columns: `x` (the state, integers from 1 to 100) and `p` (the empirical probability of being in state `x`).

Your tasks are:
1. **Solve a Non-Linear Equation:** Find the parameter $\alpha$ that satisfies the equation:
   $$ \sum_{x=1}^{100} \exp(\alpha \sqrt{x}) = 10^{20} $$
   *Note: Directly evaluating this equation will cause numerical overflow for typical floating-point numbers. You must use a numerically stable approach (e.g., transforming the equation into log-space and using functions like `logsumexp`) to find the root.* Use a numerical solver to find $\alpha$ in the range $[0, 10]$.

2. **Generate Theoretical Distribution:** Using the $\alpha$ you found, compute the theoretical probability distribution $Q(x)$ for $x \in \{1, \dots, 100\}$:
   $$ Q(x) = \frac{\exp(\alpha \sqrt{x})}{\sum_{k=1}^{100} \exp(\alpha \sqrt{k})} $$
   Ensure your calculation of $Q(x)$ is also numerically stable to avoid overflow or underflow.

3. **Compute Distance Metrics:** 
   Compare the empirical distribution $P$ (from the CSV) and the theoretical distribution $Q$. Calculate:
   - The Kullback-Leibler divergence $D_{KL}(P \parallel Q) = \sum_{x} P(x) \log(P(x) / Q(x))$
   - The Wasserstein-1 distance between the two distributions over the states $X$. Use the 1D Wasserstein distance metric where the points are the $x$ values, weighted by their respective probabilities $P$ and $Q$.

4. **Output Results:** Save your results to a JSON file located at `/home/user/results.json`. The file must have exactly this structure:
```json
{
  "alpha": 4.5678,
  "kl_divergence": 0.1234,
  "wasserstein_distance": 1.2345
}
```
Round all numbers to 6 decimal places. Use Python for your calculations.