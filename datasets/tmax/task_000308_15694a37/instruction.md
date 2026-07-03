You are acting as a performance engineer optimizing a black-box scientific simulation. 

We have a stripped, computationally expensive simulation binary located at `/app/sim_engine`. This binary simulates a physical process based on a grid of observational data and three control parameters, and it outputs a single scalar "energy" value to standard output. Your goal is to find the optimal control parameters `(p1, p2, p3)` that minimize this energy.

Here are the steps you need to follow:
1. **Data Reshaping and I/O**: You are provided with a raw observational dataset at `/home/user/raw_data.csv`. The file contains columns `x_index`, `y_index`, and `measurement`. You must reshape this into a 100x100 2D array and save it to an HDF5 file named `/home/user/obs_data.h5` under the dataset name `grid_data`.
2. **Simulation Interface**: The simulation binary is called via the command line:
   `/app/sim_engine <path_to_h5> <p1> <p2> <p3>`
   where `p1`, `p2`, and `p3` are floating-point parameters bounded between `-10.0` and `10.0`.
3. **Parallel Optimization**: Write a Python script `/home/user/optimize.py` that uses an optimization algorithm (e.g., from `scipy.optimize` like Differential Evolution or Nelder-Mead) to find the parameters that minimize the binary's output. Since the binary is slow, your script must evaluate the objective function in parallel (using `multiprocessing` or `mpi4py`) to speed up the search.
4. **Output**: Your script should save a JSON file at `/home/user/best_params.json` with the following structure:
   ```json
   {
       "p1": <float>,
       "p2": <float>,
       "p3": <float>,
       "energy": <float>
   }
   ```

Requirements:
- Your final output energy must be significantly minimized. The automated test will verify that your found energy is below a specific threshold.
- Make sure `/home/user/optimize.py` is fully self-contained and handles the parallel execution and file I/O properly.