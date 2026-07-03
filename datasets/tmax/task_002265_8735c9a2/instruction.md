You are a systems data scientist tasked with fixing a distributed parameter estimation pipeline. We are estimating the parameters (mean and covariance) of a 2D multivariate Gaussian distribution from streaming sensor data. 

Currently, our pipeline consists of:
1. A Flask Data API that simulates streaming sensor data.
2. A Redis cache intended to store intermediate iteration states (optional but available for your use).
3. A C++ worker that fetches data batches, updates its estimates, and checks for convergence.

The C++ worker (`/home/user/worker/estimator.cpp`) has several critical issues:
- **Near-Singular Matrix Failure:** The sensor data features are highly collinear. The current covariance update and inversion steps lack regularization, leading to NaNs or infinite values when calculating determinants and inverses. You need to implement Tikhonov regularization (add $\lambda = 10^{-4}$ to the diagonal of the covariance matrix) before inverting it or computing its determinant.
- **Missing Convergence Test:** The worker currently runs for a fixed number of iterations. You must implement a convergence test based on the Kullback-Leibler (KL) divergence. At each iteration, compute the KL divergence between the newly updated distribution ($\mathcal{N}_{new}$) and the distribution from the previous step ($\mathcal{N}_{old}$). Halt the iteration when $D_{KL}(\mathcal{N}_{new} \parallel \mathcal{N}_{old}) < 10^{-6}$.
- **Missing Distance Metric:** You must implement the 2D Gaussian KL divergence function. 
  The formula for $D_{KL}(\mathcal{N}_0 \parallel \mathcal{N}_1)$ is:
  $D_{KL} = \frac{1}{2} \left[ \text{tr}(\Sigma_1^{-1} \Sigma_0) + (\mu_1 - \mu_0)^T \Sigma_1^{-1} (\mu_1 - \mu_0) - 2 + \ln\left(\frac{|\Sigma_1|}{|\Sigma_0|}\right) \right]$

**Your Objectives:**
1. Start the background services by running `/app/start_services.sh`. This will spin up a Redis server on `127.0.0.1:6379` and the Data API on `127.0.0.1:8000`.
2. The Data API provides two endpoints:
   - `GET /data` returns a JSON array of 100 2D points `[ [x1, y1], [x2, y2], ... ]`.
   - `GET /truth` returns the ground truth parameters `{"mean": [mu_x, mu_y], "cov": [[c00, c01], [c10, c11]]}`.
3. Edit `/home/user/worker/estimator.cpp` to fix the numerical instability and implement the KL divergence logic. (The file already includes `httplib.h` and `json.hpp` for HTTP and JSON parsing).
4. Compile the worker using the provided `Makefile` in `/home/user/worker/`.
5. Run your worker. Once it converges, it must fetch the ground truth from `GET /truth` and calculate the KL divergence between your final fitted distribution and the true distribution.
6. Write ONLY the final computed KL divergence (as a single floating-point number) to `/home/user/final_kl.txt`.

Your goal is to achieve an accurate fit despite the near-singular data. An automated test will verify your output.