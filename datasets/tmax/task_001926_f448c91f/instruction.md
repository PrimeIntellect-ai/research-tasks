You are acting as a performance engineer fixing a numerical instability in a distributed scientific computing pipeline.

We have a multi-service application that simulates 2D heat diffusion using an implicit PDE solver. The architecture consists of:
1. **Redis** (caching layer)
2. **Python Flask Service** (`/app/frontend/app.py`): Serves as the user-facing API and caches results. Listens on `127.0.0.1:5000`.
3. **C++ Compute Engine** (`/app/engine/compute.cpp`): Solves linear systems $Ax = b$ for the implicit step. Listens on `127.0.0.1:8080`.

**The Problem:**
Our C++ compute engine currently uses a basic matrix inversion strategy to solve $Ax = b$. When researchers submit simulations with highly anisotropic materials or specific boundary conditions, the matrix $A$ becomes near-singular. This causes the standard solver to produce NaNs or wildly unstable results, crashing the pipeline.

**Your Objectives:**

1. **Fix the C++ Numerical Engine:**
   - Edit `/app/engine/compute.cpp`.
   - Update the `/solve` HTTP POST endpoint. It currently receives a JSON payload `{"A": [[...]], "b": [...]}` and responds with `{"x": [...]}`.
   - Implement a numerical stability check using the Eigen library (already included in the source tree). Calculate the absolute value of the determinant of matrix $A$.
   - If $|\det(A)| < 10^{-5}$, you must apply Tikhonov regularization before solving: modify $A$ by adding $10^{-6}$ to all elements on its main diagonal ($A \leftarrow A + 10^{-6}I$).
   - Solve the system $Ax = b$ using Eigen's robust `colPivHouseholderQr()` solver instead of a direct inverse.
   - Recompile the compute engine (a `Makefile` is provided in `/app/engine/`).

2. **Service Composition & Startup:**
   - Edit `/app/start_services.sh`. It currently has missing or incorrect configuration for starting Redis, the C++ compute engine, and the Flask app.
   - Configure the script to start `redis-server` in the background.
   - Start the compiled C++ engine on `127.0.0.1:8080`.
   - Start the Flask app using Gunicorn or basic python on `127.0.0.1:5000`. The Flask app requires the environment variable `COMPUTE_URL=http://127.0.0.1:8080`.
   - Run the script so all services are active.

3. **Experimental Data Visualization:**
   - Create a Python script `/home/user/visualize.py` that acts as an automated pipeline test.
   - The script must send an HTTP POST request to `http://127.0.0.1:5000/simulate` with JSON payload `{"size": 10, "anisotropy": 0.99999}` (which triggers the near-singular matrix path).
   - The Flask app will return a JSON response containing `{"state": [...]}` (a 100-element 1D array representing a 10x10 grid).
   - Reshape this array to 10x10 and use `matplotlib` to plot it as a heatmap.
   - Save the plot to `/home/user/heatmap.png`.

Ensure all services remain running in the background so they can be verified.