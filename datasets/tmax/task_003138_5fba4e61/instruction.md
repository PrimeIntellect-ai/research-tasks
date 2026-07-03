You are acting as a research assistant for a computational physics lab. We have a set of simulated trajectory outputs for a damped harmonic oscillator experiment. However, our simulation software occasionally produces non-physical artifacts or un-damped (runaway) trajectories due to numerical instability. 

Your goals are to:
1. **Fix and install our internal analysis package.** We have a proprietary package located at `/app/phys_fit-1.2.0` that contains standard fitting routines for our lab. Unfortunately, the person who uploaded it made a typo in its packaging configuration, preventing it from being installed. Find the bug in the package configuration, fix it, create a Python virtual environment at `/home/user/venv`, and install the package into this environment. 
2. **Build an anomaly detector.** Write a Python script at `/home/user/classify_sims.py` that processes a directory of simulation CSVs and flags the physically valid ones. 

The script `/home/user/classify_sims.py` must have the following CLI signature:
`python /home/user/classify_sims.py --input-dir <path_to_csv_directory> --output-json <path_to_output.json>`

**Classification Rules:**
For each CSV file (which contains columns `t` and `x` representing time and position):
1. Compute the velocity $v = dx/dt$ and acceleration $a = dv/dt$ using standard numerical differentiation (e.g., forward/central differences as appropriate, or `numpy.gradient`). 
2. A trajectory is **invalid** if its maximum absolute numerical acceleration $|a|$ exceeds `50.0` at any point (this indicates a numerical glitch).
3. Import `from phys_fit.oscillator import fit_damped_curve`. Call `params = fit_damped_curve(t, x)` which returns a dictionary `{'A': float, 'gamma': float, 'omega': float, 'phi': float}` representing the fit $x(t) = A e^{-\gamma t} \cos(\omega t + \phi)$. 
4. A trajectory is **invalid** if its damping coefficient $\gamma \le 0$ (this indicates a runaway/un-damped simulation).
5. If a trajectory passes both checks ($|a| \le 50.0$ everywhere AND $\gamma > 0$), it is **valid**.

The output JSON must be a single dictionary mapping the base filename (e.g., `sim_01.csv`) to a boolean: `true` if valid, `false` if invalid.

Ensure your code handles numerical edge cases gracefully. You can assume `numpy` and `scipy` are available.