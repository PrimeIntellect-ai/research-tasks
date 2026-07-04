You are a data scientist analyzing the degradation kinetics of a synthesized protein variant. You need to extract sequence and structural features from bioinformatics files, use them to parameterize an Ordinary Differential Equation (ODE), and fit the ODE to observed time-series data using Markov Chain Monte Carlo (MCMC).

Write a Bash script at `/home/user/run_analysis.sh` and a Python script at `/home/user/fit_kinetics.py` to automate this workflow.

**Phase 1: Parsing Bioinformatics Data (Bash)**
Your bash script (`/home/user/run_analysis.sh`) must:
1. Parse `/home/user/data/protein.fasta`. Extract the protein sequence (ignoring the header starting with `>`) and count the total number of Cysteine (`C`) residues. Let this integer be `N_C`.
2. Parse `/home/user/data/protein.pdb`. Count the number of lines that start with `ATOM`, represent the residue `CYS`, and have the atom name `SG`. Let this integer be `N_SG`.
3. Compute the stability factor $S = N_{SG} / N_C$ (as a floating-point number).
4. Execute your Python script, passing $S$ as a command-line argument: `python3 /home/user/fit_kinetics.py $S`

**Phase 2: ODE Solving and MCMC Fitting (Python)**
Your Python script (`/home/user/fit_kinetics.py`) must:
1. Accept the stability factor $S$ as the first command-line argument.
2. Read the observed time-series data from `/home/user/data/kinetics.csv` (which has a header `time,concentration`).
3. Define the protein degradation ODE: 
   $$ \frac{dP}{dt} = -k \cdot \frac{P^2}{1 + S} $$
   where $P(0) = 100.0$ is the initial concentration. You must use `scipy.integrate.solve_ivp` or `odeint` for numerical integration.
4. Perform MCMC sampling (you may use a custom Metropolis-Hastings implementation or `pip install emcee` to use the `emcee` package) to estimate the posterior distribution of the decay rate parameter $k$.
   - **Prior:** Uniform distribution between 0.01 and 0.5.
   - **Likelihood:** Assume the observed concentrations are normally distributed around the ODE solution with a fixed standard deviation $\sigma = 2.0$.
   - **Sampling:** Run enough steps (e.g., 5000+ samples, discarding the first 20% as burn-in) to converge.
5. Calculate the posterior mean of $k$.
6. Write the exact string format `Estimated k: X.XXX` to `/home/user/results.txt`, where `X.XXX` is the posterior mean rounded to exactly 3 decimal places.

**Environment constraints:**
- You may use `pip install --user scipy numpy emcee pandas` if needed.
- Ensure `/home/user/run_analysis.sh` is executable and is the main entry point you run to complete the task.