You are a bioinformatics analyst tasked with modeling the degradation and mutation of a specific genetic marker over time. You have raw sequence data at various time points and need to extract the marker frequency, model its dynamics using an Ordinary Differential Equation (ODE), and estimate the model parameters using Markov Chain Monte Carlo (MCMC).

Perform the following steps:

1. **Compile the Processing Tool**: 
   You have been provided with the source code for a custom sequence processing tool at `/home/user/src/seq_processor.c`. 
   Compile this C program using `gcc` and output the executable to `/home/user/bin/seq_processor` (create the directory if it does not exist). The tool does not require any special libraries besides standard C libraries.

2. **Process the Sequences**:
   Run the compiled executable on the raw sequence dataset located at `/home/user/data/sequences.txt`:
   `/home/user/bin/seq_processor /home/user/data/sequences.txt > /home/user/measurements.csv`
   The output CSV will have two columns: `time` and `marker_freq`.

3. **Mathematical Modeling**:
   The marker frequency $M(t)$ is hypothesized to follow the ODE:
   $dM/dt = \alpha \cdot M(t) - \beta \cdot t$
   where $t$ is the time, $\alpha$ is the growth rate, and $\beta$ is a time-dependent decay coefficient.
   You must use numerical integration (`scipy.integrate.solve_ivp` using the default 'RK45' method) to simulate this model. Use the first measurement (at $t=0$) as the initial condition $M(0)$.

4. **MCMC Estimation**:
   Write a Python script at `/home/user/analyze.py` that implements a basic Metropolis-Hastings MCMC algorithm from scratch to estimate the posterior distributions of $\alpha$ and $\beta$.
   * **Priors**: Uniform prior for $\alpha \in [0.0, 2.0]$ and $\beta \in [0.0, 2.0]$.
   * **Likelihood**: Assume the observed `marker_freq` values follow a Normal distribution centered on the ODE solution $M(t)$ at the corresponding times, with a fixed standard deviation $\sigma = 0.1$.
   * **Proposal Distribution**: Normal distribution centered on the current parameter value with a standard deviation of $0.05$ for both parameters.
   * **Initial State**: $\alpha = 0.5$, $\beta = 0.5$.
   * **Iterations**: 5,000 total iterations.
   * **Burn-in**: Discard the first 1,000 iterations before calculating the mean.
   * **Randomness**: Set `numpy.random.seed(42)` at the very beginning of your MCMC execution to ensure reproducibility. Update the parameters sequentially or jointly, but compute the likelihood jointly. For the proposal draw, sample `alpha_prop` then `beta_prop`.

5. **Output**:
   Calculate the mean of the accepted posterior samples (after burn-in) for both parameters.
   Save the final estimated means to `/home/user/mcmc_results.json` in the following format (rounded to 4 decimal places):
   ```json
   {
       "alpha": 0.1234,
       "beta": 0.5678
   }
   ```
   Run your script to produce this output file.