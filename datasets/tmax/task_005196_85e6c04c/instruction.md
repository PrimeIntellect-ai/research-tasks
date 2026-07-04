A researcher in our lab is trying to run a Markov Chain Monte Carlo (MCMC) simulation to estimate a diffusion coefficient $\alpha$ for a 1D material model. The forward model uses a basic finite difference mesh. However, the simulation keeps crashing. 

There are two main issues you need to resolve:

1. **Observational Data Reshaping**: 
   The raw experimental data is in `/home/user/raw_obs.csv`. It has columns `id,x,value,sensor_type`. 
   You must extract only the `x` and `value` columns, sort the rows in ascending order based on the `x` coordinate, and save this cleaned data to `/home/user/clean_obs.txt` as a space-separated file (no header).

2. **Near-Singular Matrix Crash**:
   The MCMC proposes various values for $\alpha$. When the random walk proposes a value of $\alpha$ very close to zero, the resulting finite difference matrix becomes near-singular, causing our naive Gaussian elimination solver to divide by zero or produce NaNs, breaking the entire MCMC chain.
   Modify the C++ solver located at `/home/user/simulation/solver.cpp`. In the `solve_system(double** A, double* b, int N)` function, add a Tikhonov regularization term (a ridge penalty) of exactly `1e-5` to every main diagonal element of the matrix `A` *before* the factorization/elimination steps begin. 

Once you have cleaned the data and fixed the solver, compile the simulation:
```bash
cd /home/user/simulation
g++ main.cpp solver.cpp -o mcmc_sim
```

Run the simulation (`./mcmc_sim`). It expects `/home/user/clean_obs.txt` to exist. 
The program will run 10,000 MCMC iterations and automatically write the posterior mean of $\alpha$ to `/home/user/posterior_mean.txt`. 

Please leave the compiled `mcmc_sim` executable in `/home/user/simulation/` and ensure `/home/user/posterior_mean.txt` is generated successfully.