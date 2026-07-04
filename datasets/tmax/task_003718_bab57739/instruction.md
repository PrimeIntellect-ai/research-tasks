You are a Machine Learning Engineer tasked with preparing a robust set of statistical labels from a noisy data pipeline. The data arrives via a local microservices architecture, but the pipeline is currently broken and the data itself requires complex statistical modeling to extract the true underlying signal.

Your objectives are:

1. **Service Orchestration**:
   The data pipeline relies on Redis and a Flask API. 
   - Start a Redis server on the default port (6379).
   - Start the Flask API located at `/app/data_api.py`. It requires the `REDIS_URL` environment variable to be set correctly (e.g., `redis://localhost:6379/0`).
   - Once running, trigger data generation by making a GET request to `http://127.0.0.1:5000/generate`.
   - Download the generated dataset as a JSON array by making a GET request to `http://127.0.0.1:5000/data` and save it to `/home/user/raw_data.json`.

2. **Statistical Modeling (MCMC & Bootstrap)**:
   The data points in `raw_data.json` are sampled from a mixture distribution:
   $$ p(x | \mu) = 0.7 \cdot \mathcal{N}(x | \mu, \sigma=2.0) + 0.3 \cdot \text{Uniform}(x | -15, 15) $$
   where $\mu$ is an unknown parameter.
   
   Write a Python script `/home/user/estimate.py` that:
   - Loads the data.
   - Uses Markov Chain Monte Carlo (MCMC) (e.g., the Metropolis-Hastings algorithm) to sample from the posterior distribution of $\mu$. Assume a prior $\mu \sim \mathcal{N}(0, 10^2)$.
   - Implements convergence testing (discard an appropriate burn-in period, ensure the chain mixes well).
   - After obtaining the stationary MCMC trace of $\mu$, compute the **posterior mean**.
   - Computes the **95% Bootstrap Confidence Interval** for this posterior mean using at least 1,000 bootstrap resamples of the post-burn-in trace.

3. **Workflow Orchestration**:
   Create a bash script `/home/user/run_pipeline.sh` that automates this workflow: fetching the data from the API and running the Python estimation script. 

4. **Outputs**:
   Your Python script must output the final results to `/home/user/final_metrics.json` with the following exact keys:
   - `"posterior_mean"`: The float value of your estimated $\mu$.
   - `"ci_lower"`: The lower bound of the 95% bootstrap CI.
   - `"ci_upper"`: The upper bound of the 95% bootstrap CI.

You are expected to write the MCMC and Bootstrap logic from scratch or using standard scientific libraries (`numpy`, `scipy`).