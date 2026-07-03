You are a data scientist tasked with debugging a Bayesian inference pipeline written in Go. The pipeline estimates a decay parameter `theta` for a non-linear process modeled by the ODE: `dy/dt = -theta * y^2`, with `y(0) = 1.0`.

We have observational data stored in a NetCDF file at `/home/user/data.nc` containing two variables: `t` (time) and `y` (observed values with some Gaussian noise).

The script `/home/user/fit.go` is supposed to:
1. Read the reference dataset from `/home/user/data.nc` using the `github.com/fhs/go-netcdf/netcdf` package.
2. Run a Metropolis-Hastings MCMC sampler to find the posterior distribution of `theta`.
3. Use a numerical integrator (Euler method) to solve the ODE for a given `theta` to compute the likelihood.

However, the pipeline is currently failing for two reasons:
1. **Numerical Divergence:** The ODE integrator is using a hardcoded, excessively large step size (`dt = 1.0`), which causes the simulation to diverge and produce NaNs. You must fix the integrator to use a smaller step size (e.g., `dt = 0.01`) or implement an adaptive step size.
2. **MCMC Logic Error:** The MCMC acceptance probability is calculated incorrectly, leading to a 0% acceptance rate.

Your task:
1. Install any necessary system dependencies for NetCDF (e.g., `libnetcdf-dev`).
2. Fix the bugs in `/home/user/fit.go` so that the numerical integrator is stable and the MCMC sampler correctly estimates the posterior of `theta`.
3. The MCMC should run for at least 10,000 iterations. Discard the first 2,000 iterations as burn-in (convergence testing).
4. Calculate the mean of the posterior samples for `theta`.
5. Write the final results to `/home/user/posterior.json` in the following format:
```json
{
  "mean_theta": 0.512,
  "acceptance_rate": 0.35
}
```

Ensure your `mean_theta` is accurate to within +/- 0.05 of the true parameter value used to generate the data, and the `acceptance_rate` is between 0.15 and 0.50.