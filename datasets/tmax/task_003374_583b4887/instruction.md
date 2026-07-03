You are acting as a bioinformatics systems analyst. We are trying to process a large dataset of gene sequences to determine the optimal degradation rates for a kinetic transcription model. 

Currently, our pipeline is broken. The provided Python script (`/home/user/simulate.py`) models mRNA concentration over time, but the numerical integrator diverges (produces `NaN` or `inf`) because it uses a naive explicit Euler method with a fixed step-size, and the system becomes stiff.

You need to perform the following steps:

1. **Dependency Installation**: Ensure `numpy`, `scipy`, and `pandas` are installed in the environment.
2. **Fix the Integrator**: Modify `/home/user/simulate.py`. Replace the custom Euler integrator with a robust, stiff ODE solver from `scipy.integrate` (e.g., `solve_ivp` with the `BDF` or `Radau` method). The ODE is $dM/dt = k_{syn} - d \cdot M(t)^2$, where $M(0)=0.0$, and we integrate from $t=0$ to $t=100$.
3. **Add Optimization (Non-linear Root Finding)**: We need to find the specific degradation rate $d$ (where $d \in [0.01, 5.0]$) that results in a final mRNA concentration $M(100)$ equal to a specific target value. Use an optimization/root-finding method from `scipy.optimize` (e.g., `brentq`) to find this $d$.
4. **Parallel Batch Processing**: We have a dataset of 50 sequences in `/home/user/sequences.csv` (Columns: `SeqID`, `k_syn`, `Target_M`). Create a master script (bash or Python multiprocessing) that runs your fixed `simulate.py` across all 50 rows in parallel to speed up execution.
5. **Output**: Your pipeline must generate a final CSV at `/home/user/optimized_results.csv` with the columns: `SeqID`, `Optimal_d`. The `Optimal_d` values should be rounded to 4 decimal places.

**Note on initial files**: 
`/home/user/simulate.py` and `/home/user/sequences.csv` have been placed in your home directory.

Please fix the simulation, find the optimal parameters, and generate the final output file.