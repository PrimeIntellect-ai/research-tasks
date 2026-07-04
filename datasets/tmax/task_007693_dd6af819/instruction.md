You are an AI assistant helping a researcher set up a scientific computing workflow for a Monte Carlo simulation.

You need to complete the following tasks:

1. **Environment Setup**: 
   - Create a Python virtual environment at `/home/user/venv`.
   - Install the following packages: `numpy`, `scipy`, `pytest`, `jupyter`, `nbformat`, and `papermill`.

2. **Simulation Module**:
   - Create a directory `/home/user/workspace`.
   - Inside it, write a Python module `mc_sim.py`.
   - In `mc_sim.py`, implement `simulate_random_walk(num_steps, num_trials, seed)`.
   - The function must simulate a 2D random walk. For each step, the walk moves a distance of 1.0 in a random direction.
   - **Crucial for reproducibility**: Use `rng = np.random.default_rng(seed)`. Generate the random angles for all trials and steps at once using `angles = rng.uniform(0, 2*np.pi, size=(num_trials, num_steps))`. Calculate the total X and Y displacements by summing the cosines and sines of these angles along the steps axis.
   - Return a 1D numpy array of length `num_trials` containing the final Euclidean distance from the origin for each trial.

3. **Regression Testing**:
   - Write a pytest file `/home/user/workspace/test_sim.py`.
   - Include a test function `test_mean_distance()` that runs `simulate_random_walk(100, 10000, 42)`.
   - The theoretical expected distance for $N$ steps is $\sqrt{N \pi / 4}$. For $N=100$, this is $5\sqrt{\pi} \approx 8.86227$.
   - Assert that the mean of the simulated distances is within `0.1` of this theoretical value.
   - Run `pytest /home/user/workspace/test_sim.py` and ensure it passes. Leave the test file in place.

4. **Notebook Orchestration**:
   - Write a Python script `/home/user/workspace/create_nb.py` that uses `nbformat` to programmatically generate a Jupyter Notebook named `/home/user/workspace/experiment.ipynb`.
   - The notebook should have two code cells:
     - **Cell 1**: Must have the tag `parameters` (so `papermill` can inject variables). It should define default variables: `num_steps = 10`, `num_trials = 100`, `seed = 42`.
     - **Cell 2**: Must import `simulate_random_walk` from `mc_sim`, run it with the notebook parameters, and perform a Kolmogorov-Smirnov (KS) test to compare the simulated distances against the theoretical Rayleigh distribution.
     - The theoretical distribution is Rayleigh with scale parameter $\sigma = \sqrt{N / 2}$. Use `scipy.stats.kstest(distances, 'rayleigh', args=(), kwds={'scale': np.sqrt(num_steps / 2.0)})`.
     - Finally, Cell 2 must write the KS statistic and p-value as a comma-separated string `"{statistic:.6f},{pvalue:.6f}"` to `/home/user/workspace/ks_result.txt`.
   - Run `create_nb.py` to generate the notebook.

5. **Execution**:
   - Use `papermill` (via your virtual environment) to execute `/home/user/workspace/experiment.ipynb` and output to `/home/user/workspace/output.ipynb`.
   - Inject the following parameters: `num_steps` = 200, `num_trials` = 25000, `seed` = 1001.

When you are done, `/home/user/workspace/ks_result.txt` should contain the correct deterministic test statistics.