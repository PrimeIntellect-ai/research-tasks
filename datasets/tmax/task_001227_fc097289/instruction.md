You are a performance engineer tasked with profiling and fixing a C-based 2D PDE solver, then exposing it via a network service for automated workflow orchestration.

A vendored package for the solver is located at `/app/pde_solver`. It contains the source code for a 2D Laplace equation solver on a square domain using finite differences. However, the package is currently broken due to a configuration/code perturbation introduced during its last update, preventing it from compiling or running correctly. 

Your objectives are:
1. **Fix the Package**: Inspect `/app/pde_solver`, identify the deliberate perturbation (e.g., broken build files or incorrect environment/macro definitions), and fix it so the C program compiles successfully into an executable named `solver`. The solver expects an integer argument `N` (the grid size) and prints the maximum error after a fixed number of iterations.
2. **Workflow Orchestration Service**: Write and start a Python-based HTTP web service listening exactly on `127.0.0.1:8000`. This service will orchestrate mesh refinement, convergence testing, and experimental data visualization.
3. **Endpoint Specification**: Create an endpoint `POST /profile` that accepts JSON requests.
    - The JSON payload will look like: `{"token": "pde-admin-token", "start_N": 8, "target_error": 0.05}`.
    - **Authentication**: If the `token` does not exactly match `"pde-admin-token"`, return an HTTP 401 Unauthorized status.
    - **Convergence Testing**: Starting with `N = start_N`, execute the compiled C `solver` program. The solver outputs a single floating-point number representing the error. If the error is greater than `target_error`, double the grid size (`N = N * 2`) and run the solver again. Repeat this mesh refinement loop until the solver's output error is less than or equal to `target_error`.
    - **Profiling**: Record the execution time (in seconds) of the C solver for each tested `N`.
    - **Visualization**: Generate a simple plot of execution time vs. `N` and save it to `/home/user/profile_plot.png`.
    - **Response**: Return an HTTP 200 JSON response with the following exact schema:
      ```json
      {
        "converged_N": <int>,
        "errors": [<float>, <float>, ...],
        "execution_times": [<float>, <float>, ...]
      }
      ```

Make sure your HTTP service remains running in the foreground or as a background daemon so that automated tools can query it. Provide the commands you would use to fix the C package, write the Python service, and start it.