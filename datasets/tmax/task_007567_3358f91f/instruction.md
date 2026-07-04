You are a performance engineer profiling a new distributed microservice architecture. A single user request passes sequentially through three independent services. The processing time for each service follows an exponential distribution with the following rates (requests per second):
- Service A: $\lambda_A = 50$
- Service B: $\lambda_B = 20$
- Service C: $\lambda_C = 10$

You need to analyze the end-to-end latency (the sum of the three processing times) by combining Monte Carlo simulation, analytical validation, and curve fitting. 

Write a Python script to perform the following steps:
1. **Analytical Validation:** Calculate the exact theoretical mean and variance of the total end-to-end response time using the properties of independent exponential distributions.
2. **Monte Carlo Simulation:** Simulate 100,000 end-to-end requests. Use `numpy` with the legacy random seed set to `42` (`numpy.random.seed(42)`) and generate the times using `numpy.random.exponential(scale, size=100000)` for each of the three services. Calculate the empirical mean and variance of the simulated total response times.
3. **Curve Fitting:** The exact distribution of the sum of these exponentials is a Hypoexponential distribution, but we want to approximate it with a Gamma distribution for our monitoring tools. Use `scipy.stats.gamma.fit` to fit a Gamma distribution to your simulated total response times. You must fix the location parameter to 0 by passing `floc=0`. Extract the fitted `shape` (often denoted as `a`) and `scale` parameters.

Save your final results in a JSON file at `/home/user/perf_analysis.json` with the following structure. All numerical values must be floats rounded to exactly 4 decimal places:
```json
{
  "theoretical_mean": 0.0000,
  "theoretical_variance": 0.0000,
  "mc_mean": 0.0000,
  "mc_variance": 0.0000,
  "gamma_shape": 0.0000,
  "gamma_scale": 0.0000
}
```