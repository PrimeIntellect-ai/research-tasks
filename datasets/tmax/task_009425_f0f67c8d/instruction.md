As a computational researcher, I am evaluating the numerical stability and convergence properties of different optimization algorithms on ill-conditioned landscapes. 

I need you to write and execute a Python script that tests the convergence of the BFGS and Nelder-Mead algorithms on the standard 2D Rosenbrock function:
$f(x,y) = (1-x)^2 + 100(y-x^2)^2$

Your task:
1. Generate 100 random starting points $(x_0, y_0)$. To test numerical stability against initial condition perturbations, draw these points from a Normal distribution with a mean of 0.0 and a standard deviation of 2.0. You MUST use `numpy` and set `numpy.random.seed(123)` immediately before generating the points with `numpy.random.normal(0.0, 2.0, (100, 2))`.
2. For each starting point, optimize the Rosenbrock function twice: once using `scipy.optimize.minimize` with `method='BFGS'` and once with `method='Nelder-Mead'`.
3. Evaluate convergence: An optimization run is considered successfully converged if the Euclidean distance between the final coordinates returned by the optimizer (`res.x`) and the known global minimum `(1.0, 1.0)` is strictly less than `1e-3`.
4. Calculate the convergence rate (number of successful convergences divided by 100) for both algorithms.
5. Output the final rates into a JSON file located precisely at `/home/user/convergence_results.json`. 

The JSON file must have exactly this structure:
```json
{
  "bfgs_convergence_rate": 0.0,
  "nm_convergence_rate": 0.0
}
```
(Replace `0.0` with the actual floating-point fractions you compute).

You have full freedom to create the script anywhere, but the final output must strictly reside at `/home/user/convergence_results.json`.