I am a quantitative researcher trying to restore an old simulation workflow. I have an image of some handwritten simulation parameters from a previous experiment, and I need to rerun the Monte Carlo simulation and compare it to historical data. 

Please automate this workflow for me by following these steps:

1. **Parameter Extraction**: 
   I have an image located at `/app/params.png`. Use OCR (e.g., `tesseract`) to extract the Geometric Brownian Motion (GBM) parameters from it. The parameters are: `S0`, `mu`, `sigma`, `T`, `Seed`, and `N_paths`.

2. **Simulation Development (Notebook-based workflow)**:
   Create a Jupyter Notebook at `/home/user/gbm_sim.ipynb`. In this notebook, write Python code to perform a Monte Carlo simulation for the final asset price $S_T$ using the parameters extracted.
   - Use the exact log-normal solution for the final time step: 
     $$S_T = S_0 \exp\left(\left(\mu - \frac{\sigma^2}{2}\right)T + \sigma \sqrt{T} Z\right)$$
   - Use `numpy` to generate the random variables. Initialize the random number generator using `np.random.seed(Seed)`.
   - Draw exactly `N_paths` standard normal variables ($Z$) using `np.random.normal(0, 1, N_paths)`.
   - Calculate the mean of the simulated final prices (`simulated_mean`).

3. **Reference Dataset Comparison**:
   Load the reference historical data located at `/app/historical.csv`. This file contains a single column `Final_Price`. Calculate the mean of these prices (`reference_mean`), and find the absolute difference between your `simulated_mean` and the `reference_mean` (`difference`).
   Execute your notebook to ensure all logic is sound and the results are computed correctly.

4. **Service Orchestration**:
   Write and run a simple HTTP server (e.g., using Flask or FastAPI) listening on `127.0.0.1:8080`. It must run continuously in the background.
   The server must expose a `GET /metrics` endpoint. When queried, it should return a JSON response containing exactly the following keys and your computed values:
   ```json
   {
     "S0": <integer>,
     "mu": <float>,
     "sigma": <float>,
     "simulated_mean": <float, rounded to 2 decimal places>,
     "reference_mean": <float, rounded to 2 decimal places>,
     "difference": <float, rounded to 2 decimal places>
   }
   ```

Make sure your HTTP server is running and accessible on port 8080 before you finish.