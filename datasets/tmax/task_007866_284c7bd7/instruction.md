You are acting as a Machine Learning Engineer preparing a robust training dataset of epidemiological parameters. 

You need to analyze a set of synthetic outbreak data using an ODE model, estimate the parameters using Markov Chain Monte Carlo (MCMC), and calculate confidence intervals using Bootstrapping. 

The observed infection data is located at `/home/user/observations.csv`, which contains two columns: `day` and `infected`.

Your task is to write a script, `/home/user/analyze_sir.py`, that performs the following steps and saves the final metrics.

**1. ODE Numerical Solving (SIR Model)**
Implement the SIR (Susceptible-Infected-Recovered) model using `scipy.integrate.odeint`.
The equations are:
$dS/dt = -\beta S I$
$dI/dt = \beta S I - \gamma I$
$dR/dt = \gamma I$
Use initial conditions: $S(0) = 0.99$, $I(0) = 0.01$, $R(0) = 0.0$.
Time steps should exactly match the `day` column in the observations file.

**2. MCMC Posterior Estimation**
Implement a Metropolis-Hastings MCMC algorithm to estimate the posterior distributions of $\beta$ and $\gamma$.
- Use a Gaussian random walk proposal: $\beta_{new} \sim N(\beta_{current}, \sigma=0.05)$ and $\gamma_{new} \sim N(\gamma_{current}, \sigma=0.05)$.
- The log-likelihood should be the negative Sum of Squared Errors (SSE) between the observed `infected` values and the ODE-predicted $I$ values.
- Use uniform priors: $\beta \in [0.1, 2.0]$ and $\gamma \in [0.01, 1.0]$. If a proposal falls outside this range, its prior probability is 0 (log-prior = $-\infty$).
- Initialize the chain at $\beta_0 = 0.5, \gamma_0 = 0.1$.
- Run exactly 5,000 MCMC iterations.
- Discard the first 1,000 iterations as burn-in.
- **CRITICAL for reproducibility:** Before starting the MCMC loop, set `numpy.random.seed(42)`. Call `np.random.normal()` twice per iteration to generate the proposals for $\beta$ and $\gamma$ (in that order), and then call `np.random.uniform()` once to make the acceptance decision.

**3. Bootstrap Confidence Intervals**
Using the remaining 4,000 accepted/rejected MCMC samples, calculate the Basic Reproduction Number $R_0 = \beta / \gamma$ for each sample.
Then, perform non-parametric bootstrapping:
- Resample the 4,000 $R_0$ values 10,000 times with replacement.
- **CRITICAL for reproducibility:** Before starting the bootstrap loop, set `numpy.random.seed(123)`.
- For each bootstrap resample, calculate the mean $R_0$.
- Find the 95% Confidence Interval (2.5th and 97.5th percentiles) of these bootstrap means using `numpy.percentile`.

**Output**
Save the final results to `/home/user/training_meta.json` with the following exact keys:
```json
{
  "beta_mean": <mean of post-burn-in beta samples>,
  "gamma_mean": <mean of post-burn-in gamma samples>,
  "R0_ci_lower": <2.5th percentile of bootstrap means>,
  "R0_ci_upper": <97.5th percentile of bootstrap means>
}
```
Ensure all values are standard floats (not numpy types) so they serialize correctly to JSON.