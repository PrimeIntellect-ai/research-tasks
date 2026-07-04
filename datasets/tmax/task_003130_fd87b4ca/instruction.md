You are assisting a researcher modeling the kinetics of a stiff chemical reaction. The researcher has an automated experimental setup, but the parameter estimation pipeline is currently broken.

You are given the following in your environment:
1. `/app/blackbox_reactor`: A stripped executable that simulates the exact, true kinetics of the reaction. It takes three kinetic rate constants as arguments (`k1`, `k2`, `k3`) and outputs a raw, unformatted stream of concentrations over time.
2. `/home/user/pipeline/data/raw_experiment.dat`: A file containing the raw experimental observations from the true system (with unknown parameters). The data is noisy and irregularly formatted.
3. `/home/user/pipeline/integrate.py`: A Python script containing an explicit RK4 integrator. It currently diverges and produces `NaN`s because the chemical system is highly stiff, and the fixed step-size adaptation is flawed.

Your objective is to complete the parameter estimation workflow:
1. **Observational Data Reshaping**: Write a Bash script (`/home/user/pipeline/clean_data.sh`) that parses `raw_experiment.dat`, removes comments, standardizes the delimiters to commas, interpolates to a regular grid of 100 time points between $t=0$ and $t=100$, and saves it as `/home/user/pipeline/data/clean_experiment.csv` (columns: `time,A,B,C`).
2. **Numerical Integration**: Fix `/home/user/pipeline/integrate.py`. You must modify it to use an implicit solver or an adaptive stiff solver (e.g., BDF or Radau via SciPy) so it correctly integrates the ODEs without diverging. The ODEs are:
   $dA/dt = -k_1 A + k_2 B C$
   $dB/dt = k_1 A - k_2 B C - k_3 B^2$
   $dC/dt = k_3 B^2$
   Initial conditions: $A(0)=1, B(0)=0, C(0)=0$.
3. **MCMC Sampling & Pipeline**: Create a master Bash script (`/home/user/pipeline/run_mcmc.sh`) that orchestrates a Metropolis-Hastings MCMC sampler (you can write an auxiliary Python script for the sampling logic). The sampler must use your fixed `integrate.py` to evaluate the likelihood of proposed parameters `k1, k2, k3` against `clean_experiment.csv`. Use a Gaussian likelihood with $\sigma=0.05$.
4. **Integration**: Run your pipeline to generate at least 5000 accepted MCMC samples (discard the first 20% as burn-in). The final output of `run_mcmc.sh` must write a file at `/home/user/pipeline/results/posterior_means.csv` containing exactly one line with the comma-separated posterior means of `k1`, `k2`, and `k3`.

The automated verifier will evaluate the accuracy of your derived posterior means by feeding them back into `/app/blackbox_reactor` and measuring the Mean Squared Error (MSE) of the resulting trajectory against the true noiseless trajectory.