You are assisting a researcher who is running a molecular network simulation. The simulation tool calculates collision densities based on molecular graph models. However, the current setup has several issues:

1. The simulation library source code, vendored at `/app/graph-sim-1.0`, fails to compile.
2. Even when it does compile, the results of the molecular density simulation are non-reproducible across identical runs due to floating-point reduction order issues in the multi-threaded aggregation loop.
3. The researcher needs an HTTP REST API to automatically run the simulation, fit a normal distribution (compute mean and standard deviation) on the output, compare it to a reference dataset, and serve the results.

Your task:
1. Navigate to `/app/graph-sim-1.0` and fix the compilation process. The project uses a standard `Makefile`, but it has been corrupted.
2. Fix the non-reproducibility bug in `src/simulator.cpp`. The function `aggregate_nodes` calculates a sum across graph nodes using OpenMP or multi-threading, which causes non-deterministic floating-point accumulation. You must modify the code to ensure deterministic, reproducible results (for example, by enforcing an ordered reduction or sorting the array before summing).
3. Write an API server in Python (or another language of your choice) and save it at `/home/user/server.py`.
4. Run this API server. It must listen on `127.0.0.1:9090`.
5. The API must expose an endpoint `POST /simulate`.
   - It must require a header: `X-API-Key: moleculardynamics42`.
   - When requested, the server must execute the compiled binary `/app/graph-sim-1.0/bin/simulate_graph /app/molecule_graph.dat`.
   - The binary outputs a list of floating-point density values (one per line).
   - Your server must calculate the mean and population standard deviation of these values.
   - It must read the reference values from `/app/reference_data.csv` (which contains a single line with `ref_mean,ref_std`).
   - The endpoint must return a JSON response in the exact format:
     ```json
     {
       "sim_mean": <float>,
       "sim_std": <float>,
       "diff_mean": <sim_mean - ref_mean>,
       "diff_std": <sim_std - ref_std>
     }
     ```
     (Round all values in the JSON to 4 decimal places).

Ensure the server is left running in the background so that it can be tested by our automated verification suite.