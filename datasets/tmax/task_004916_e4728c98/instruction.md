You are helping a computational chemistry researcher debug and deploy a simulation workflow. The researcher has been trying to run an MCMC (Markov Chain Monte Carlo) parameter estimation for a simple ordinary differential equation (ODE) modeling a chemical degradation process, followed by a Monte Carlo forward projection.

However, their current pipeline is broken, and their forward projections suffer from floating-point accumulation errors due to chaotic parallel reduction orders.

Here is your task:

1. **Extract Observational Data (OCR & Reshaping):**
   There is an image file located at `/app/observational_data.png`. It contains a scanned table of experimental observations. Use OCR (e.g., `tesseract`) to extract the data. The image contains two columns: `Time` and `Concentration`. Reshape this data into a structured CSV file at `/home/user/extracted_data.csv`.

2. **MCMC Parameter Estimation (Go):**
   The chemical process follows the ODE: 
   $dC/dt = -k \cdot C$
   where $C$ is the Concentration and $k$ is the unknown degradation rate. 
   Write a Go program that reads your extracted CSV. Assume the initial concentration $C(0)$ is the value at Time 0.
   Implement a basic Metropolis-Hastings MCMC algorithm in Go to estimate the posterior mean of the parameter $k$. 
   - Use a Gaussian likelihood function with $\sigma = 1.0$.
   - Use a Uniform(0, 1) prior for $k$.
   - Run the chain for 100,000 steps (burn-in 10,000 steps).

3. **Monte Carlo Forward Projection & The Floating-Point Fix:**
   The researcher wants to predict the expected concentration at a future time $T$ by sampling $k$ from the MCMC chain's posterior (using the last 1,000 samples). For each of the 1,000 samples, solve the ODE numerically (using simple Euler integration with step size $dt=0.1$) up to time $T$ to get $C(T)$.
   *CRITICAL FIX:* To fix the researcher's floating-point non-reproducibility issues, you must compute the final expected value (mean of the 1,000 predictions) by **sorting the 1,000 floating-point predictions in strictly ascending order** before summing them up and dividing by 1,000. 

4. **Expose as a Web Service:**
   Create a Go HTTP server listening on `0.0.0.0:8080`.
   - It must require an `Authorization` header with the exact value `Bearer chem-sim-2024`.
   - Endpoint: `POST /predict`
   - Request Body (JSON): `{"time": 5.0}` (where `time` is the future time $T$ to predict).
   - Response Body (JSON): `{"expected_concentration": 12.345}` (using the sorted-sum Monte Carlo projection described above).

Ensure your Go server is compiled and left running in the background (or foreground if you prefer, but the system must be able to test it). Write all code in `/home/user/sim`.