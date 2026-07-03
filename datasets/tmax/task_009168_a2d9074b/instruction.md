You are helping a computational biophysics researcher fix and run a structural simulation pipeline. The current pipeline extracts structural features from a protein, but the downstream numerical integrator is diverging due to a naive fixed-step implementation, ruining the ensemble analysis. 

Your objective is to fix the numerical integrator, implement a parallel simulation ensemble, and package the workflow into a reproducible pipeline.

**Phase 1: Feature Extraction (Bioinformatics & Matrix Decomposition)**
1. Write a script `/home/user/extract_svd.py`. 
2. It must read the PDB file located at `/home/user/data/input.pdb` and extract the 3D coordinates (x, y, z) of all Alpha Carbon atoms (atom name `CA`). 
3. Build an $N \times 3$ coordinate matrix, then compute the $N \times N$ pairwise Euclidean distance matrix $D$ between all CA atoms.
4. Perform Singular Value Decomposition (SVD) on $D$. Find the maximum singular value ($\sigma_{max}$) and save it as a float, rounded to 4 decimal places, to `/home/user/results/svd_max.txt`.

**Phase 2: Fixing the Numerical Integrator**
The file `/home/user/sim/integrator.py` contains a `simulate(k, t_end)` function that models structural relaxation governed by the ODE: $\frac{dy}{dt} = -k \cdot y$, with initial condition $y(0) = 100.0$. 
Currently, it uses a naive forward Euler method with a fixed `dt=0.5`. For large $k$, this step size causes the simulation to oscillate and diverge to infinity!
*   **Task:** Modify `/home/user/sim/integrator.py`. Rewrite the `simulate(k, t_end)` function to use `scipy.integrate.solve_ivp` with the `'RK45'` method (which has adaptive step-size) to solve the ODE accurately. The function must return the final simulated value of $y$ at $t = t\_end$ as a python `float`.

**Phase 3: Parallel Ensemble Simulation**
1. Write `/home/user/sim/run_ensemble.py`.
2. This script must read $\sigma_{max}$ from `/home/user/results/svd_max.txt`.
3. We need to run simulations for different scaling factors $c \in [0.5, 1.0, 1.5, 2.0]$. For each $c$, the decay rate is $k = c \cdot \sigma_{max}$.
4. Use Python's `multiprocessing.Pool` with 4 workers to run the `simulate(k, t_end=5.0)` function in parallel for all 4 values of $k$.
5. Save the results to `/home/user/results/ensemble_final.json` as a JSON dictionary mapping the string representation of $c$ to the final $y$ value (e.g., `{"0.5": 12.345, "1.0": ...}`).

**Phase 4: Reproducible Pipeline**
Create a bash script at `/home/user/run_pipeline.sh` that executes the whole workflow from scratch:
1. Creates the `/home/user/results` directory if it doesn't exist.
2. Runs `/home/user/extract_svd.py`.
3. Runs `/home/user/sim/run_ensemble.py`.

Ensure your scripts are fully self-contained and executable. The container environment already has `numpy` and `scipy` installed.