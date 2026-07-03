You are a bioinformatics analyst working on a metabolic pathway simulation pipeline. The system is a multi-service architecture located in `/app/`, consisting of a Python FastAPI web server, a Redis message broker, and a C++ ODE compute worker. 

Currently, the system is broken in a few ways:
1. **Service Configuration**: The services are not communicating correctly. You need to fix the environment variables or configuration files so that the API server (running on port 8000) and the C++ worker can both communicate via Redis (running on port 6379). The startup script is `/app/start_services.sh`.
2. **Numerical Divergence**: The C++ compute worker (`/app/worker/integrator.cpp`) simulates enzyme kinetics using an adaptive Runge-Kutta (RK45) method. However, the step-size adaptation logic is flawed, causing the simulation to diverge or return `NaN` for stiff equations. You must fix the adaptive step-size logic, ensure the error control works correctly, and recompile the worker using the provided `Makefile`.
3. **Parameter Optimization**: Once the pipeline is functional, use it to fit the kinetic parameters (`k1`, `k2`, `k3`) to the observed experimental data provided in `/app/data/observed.csv`. You may write a Python script using optimization routines (e.g., SciPy's `minimize` or `curve_fit`) to find the best parameters that minimize the Mean Squared Error (MSE) between the simulated Product `P` concentrations and the observed `P` over time.

The API exposes a `POST /simulate` endpoint that expects a JSON payload: `{"k1": <float>, "k2": <float>, "k3": <float>}` and returns the simulated time-series data.

**Requirements:**
- Fix the inter-service communication and the numerical integrator bug.
- Perform the parameter optimization.
- Save your final optimized parameters in a valid JSON file at `/home/user/best_params.json` with the keys `"k1"`, `"k2"`, and `"k3"`.
- Do not stop the services when you are finished; they must be running for the evaluation.

Ensure that your optimized parameters produce an MSE of less than 0.01 against the observed data for the Product `P`.