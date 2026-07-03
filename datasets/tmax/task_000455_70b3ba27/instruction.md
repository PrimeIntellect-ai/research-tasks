I need your help fixing and orchestrating a molecular simulation workflow I've been building. Right now, it consists of a Python-based compute API and a Redis cache, but the mathematical core is crashing and the services aren't glued together properly.

The codebase is located at `/home/user/molecule_sim/`. It is meant to simulate the diffusion of energy across a molecular network (represented as a graph) using continuous-time Markov chains, but it's failing when the transition matrix is near-singular (which happens because my molecule graph has weakly connected symmetries).

Here is what you need to do:

1. **Fix the Numerical Instability**: 
   In `/home/user/molecule_sim/calc.py`, the `solve_steady_state` function tries to invert a Laplacian matrix to find the fundamental matrix. This fails with a `LinAlgError` due to near-singularity. Modify the code to handle this by applying a Tikhonov regularization (add an identity matrix multiplied by `1e-6` to the Laplacian before inversion).

2. **Implement Numerical Integration & Bootstrapping**:
   Update the `compute_diffusion` function in `calc.py`. It takes an initial state vector. You must:
   - Numerically integrate the state probabilities from $t=0$ to $t=5.0$ using `scipy.integrate.odeint` or `solve_ivp` given the differential equation $dP/dt = -L \cdot P$ (where $L$ is the regularized Laplacian).
   - Perform a bootstrap analysis: generate 500 bootstrap samples of the provided initial state vector (sampling with replacement the indices of the initial distribution), run the numerical integration for each sample to get the final state vector at $t=5.0$, and calculate the 2.5th and 97.5th percentiles (95% confidence interval) for each node's final probability.

3. **Service Orchestration**:
   The system relies on a Redis server and a Flask API. 
   - Start a local Redis instance listening on `127.0.0.1:6379`. (A configuration file `/home/user/molecule_sim/redis.conf` is provided; you must ensure the Redis process runs in the background using it).
   - The Flask app (`/home/user/molecule_sim/api.py`) needs to connect to Redis. Set the environment variable `REDIS_URL=redis://127.0.0.1:6379/0`.
   - Start the Flask app so it listens on `127.0.0.1:8080`.

4. **API Endpoints**:
   Ensure `api.py` exposes a `POST /simulate` endpoint that accepts JSON: `{"initial_state": [0.5, 0.2, 0.1, 0.2]}`.
   The endpoint must:
   - Call your fixed calculation pipeline.
   - Save the resulting lower and upper confidence bounds in Redis as a JSON string under the key `latest_bounds`.
   - Return a JSON response: `{"status": "success", "lower_ci": [...], "upper_ci": [...]}`.

Please make the necessary code changes, configure the environment, and leave both the Redis service and the Flask API running continuously in the background. Do not wrap the background processes in a script that exits; make sure they are listening on the specified ports before you finish.