You are a machine learning engineer tasked with preparing and analyzing training data from a dual-sensor system. The raw data is noisy and unformatted, and you must build a reproducible pipeline to clean it, compare the sensors, and estimate the underlying signal parameters using MCMC.

Your tasks are to:

1. **Reshape the Data**: 
   You have a raw, interleaved dataset at `/home/user/raw_observations.txt`. Each line contains `sensor_id, x, y`. 
   Write a Python script to parse this file and align the readings. Create a cleaned CSV at `/home/user/cleaned_dataset.csv` with columns `x, y1, y2` (where `y1` is from sensor `S1` and `y2` is from sensor `S2`, sorted by `x` ascending).

2. **Statistical Hypothesis Testing**:
   Perform a paired T-test between `y1` and `y2` to determine if the sensors have a statistically significant bias difference. 

3. **MCMC Parameter Estimation**:
   Assume the true signal follows a linear model: $y = m \cdot x + c$. 
   Using the `emcee` Python package, perform an MCMC sampling to estimate the posterior distribution of $m$ and $c$ using *only* the data from sensor `S1` (`y1`).
   - Use a Gaussian likelihood function with a fixed standard deviation $\sigma = 0.5$.
   - Use uniform (flat) priors: $m \in [0, 5]$ and $c \in [-5, 5]$.
   - Use 10 walkers.
   - Initialize the walkers with a tight Gaussian ball around $m=2.0, c=1.0$ with standard deviation $0.01$.
   - **Crucial for reproducibility:** Set `numpy.random.seed(42)` immediately before initializing the walkers' starting positions and before running the sampler.
   - Run the sampler for 2000 steps. Discard the first 500 steps as burn-in.

4. **Reproducible Pipeline**:
   Create a bash script at `/home/user/run_pipeline.sh` that:
   - Installs any necessary dependencies (like `emcee`, `scipy`, `pandas`).
   - Runs your Python script to generate `cleaned_dataset.csv` and a results file.

5. **Output Results**:
   Your Python script must output a JSON file at `/home/user/results.json` containing the exact following keys:
   - `"p_value"`: The p-value from the paired T-test between `y1` and `y2`.
   - `"m_mean"`: The mean of the flattened MCMC posterior chain for $m$ (after burn-in).
   - `"c_mean"`: The mean of the flattened MCMC posterior chain for $c$ (after burn-in).

Ensure your bash script is executable (`chmod +x`). 
You may use the terminal to write, test, and debug your scripts.