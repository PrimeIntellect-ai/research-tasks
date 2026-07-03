You are a performance engineer working on a molecular network diffusion simulation tool. We have a vendored package located at `/app/mol_sim_net-1.0.0` that performs numerical integration of diffusion processes over graph structures (representing molecular interactions). 

Recently, our continuous integration pipeline failed because the adaptive step-size integrator within this package diverges completely on stiff graphs, causing infinite loops or NaNs instead of converging. 

Your tasks are as follows:

1. **Fix the Vendored Package:**
   Analyze the adaptive step-size logic in the integrator located in `/app/mol_sim_net-1.0.0/mol_sim_net/integrator.py`. The ODE is $\frac{dx}{dt} = -L x$, where $L$ is the graph Laplacian. There is a mathematical bug in how the new step size (`dt_new`) is calculated based on the error estimate and the tolerance (`tol`). Fix the step-size adaptation formula so the solver shrinks the step size when the error is too high, and grows it when the error is low. 

2. **Serve the Simulation (REST API):**
   Once the package is fixed and installed in your environment, create and start an HTTP server (e.g., using Flask or FastAPI) listening on `127.0.0.1:8080`. 
   
   The server must expose a single `POST` endpoint at `/simulate`.
   
   **Authentication:** 
   The server must require an `Authorization` header with the exact value: `Bearer sim_token_99`. If the token is missing or incorrect, return an HTTP 401 Unauthorized status.
   
   **Request format:**
   A JSON payload containing:
   - `edges`: A list of pairs `[u, v]` representing undirected edges of the graph.
   - `initial_state`: A list of floats representing the initial concentration at each node (ordered by node index 0, 1, ..., N-1).
   - `t_end`: A float representing the end time of the simulation.
   - `tol`: A float representing the error tolerance.
   
   **Processing:**
   Compute the graph Laplacian $L$ for the given edges (assume unweighted, undirected edges). Use the fixed `integrate_diffusion` function from the `mol_sim_net` package to calculate the final state at `t_end`.
   
   **Response format:**
   Return a JSON response with HTTP 200 OK containing:
   - `final_state`: A list of floats representing the state of each node at `t_end` (rounded to 4 decimal places).

Leave the server running in the background or foreground so that our automated test suite can verify the API. You may use `pip` to install any necessary web frameworks.