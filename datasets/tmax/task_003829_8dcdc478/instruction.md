You are a performance engineer tasked with optimizing a legacy scientific computing pipeline. 

We have a stripped legacy binary located at `/app/oracle_mcmc` that performs Metropolis-Hastings MCMC sampling to estimate the posterior distribution of two parameters $(a, b)$ for a nonlinear model. The model equations are known:
$y_i = a \cdot \exp(-b \cdot x_i) + \epsilon_i$
where $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$ with known $\sigma = 0.5$. 
The prior distributions are uniform: $a \sim \mathcal{U}(0, 10)$ and $b \sim \mathcal{U}(0, 5)$.

The legacy binary reads an input file of observations at `/app/data.csv` (format: `x,y` on each line) and generates 100,000 MCMC samples, saving them to `oracle_samples.csv` (format: `a,b`). It is notoriously slow because it runs a single chain sequentially. 

Your objectives:
1. **Parallel MCMC Implementation**: Write a C++ program at `/home/user/fast_mcmc.cpp` that implements an equivalent Metropolis-Hastings sampler for this model.
    - Use OpenMP to run 4 independent MCMC chains in parallel.
    - Each chain should generate 25,000 samples (to reach the same total of 100,000).
    - Combine the samples into a single output file `fast_samples.csv`.
    - You must achieve at least a **3.0x speedup** compared to the legacy binary.
2. **Notebook Workflow Orchestration**: Create a Jupyter notebook at `/home/user/workflow.ipynb` that:
    - Compiles your C++ code (e.g., using `g++ -O3 -fopenmp ...`).
    - Profiles the execution time of `/app/oracle_mcmc` and your `./fast_mcmc`.
    - Loads `oracle_samples.csv` and `fast_samples.csv`.
    - Performs density estimation (e.g., KDE) to compare the posteriors visually.
    - Computes and prints the sample means of $a$ and $b$ for both methods to verify correctness.

You have sudo access to install `g++`, `libomp-dev`, Python data science packages (`jupyter`, `pandas`, `scipy`, `matplotlib`), or any other dependencies.

Constraints:
- Your C++ program must accept the input data path and output samples path as command line arguments: `./fast_mcmc /app/data.csv /home/user/fast_samples.csv`.
- The sample means of your $a$ and $b$ estimates must be within 0.05 of the oracle's estimates.