You are a machine learning engineer preparing a training dataset of dynamical system trajectories for a Neural ODE model. The data generation pipeline relies on a C++ Monte Carlo ODE integrator that parallelizes simulations using OpenMP, coordinates tasks via Redis, and aggregates the results into an HDF5 file through a Python REST API. 

However, the current pipeline is broken:
1. The C++ numerical integrator (`/home/user/workspace/mc_integrator.cpp`) diverges. It attempts to implement a standard 4th-order Runge-Kutta (RK4) method to solve the damped oscillator system:
   dx/dt = y
   dy/dt = -k*x - c*y
   There is a bug in the step-size calculation or the RK4 coefficients. You need to fix it. The program takes `k`, `c`, `x0`, `y0`, and `N_mc` (Monte Carlo samples) as command-line arguments. It applies small random Gaussian perturbations to `x0, y0` (already implemented), runs the RK4 integration to t=5.0 with dt=0.01, and prints the averaged final state `x_final y_final` to stdout.
2. The data aggregation service (`/home/user/workspace/api_server.py`) is misconfigured. It needs to be connected to the Redis parameter server and configured to invoke your compiled C++ binary using `mpirun`.
3. You need to orchestrate the workflow using the provided Jupyter notebook (`/home/user/workspace/workflow.ipynb`), which sends API requests to the Python service to kick off the generation and verifies the resulting HDF5 file.

Your tasks:
1. Fix the bug in `/home/user/workspace/mc_integrator.cpp`. Compile it to `/home/user/workspace/mc_worker` (ensure you link OpenMP).
2. Edit `/home/user/workspace/api_server.py` to point to the correct Redis instance (running on `localhost:6379`) and configure the worker path to `/home/user/workspace/mc_worker`.
3. Start the Redis server, the Python Flask API server (on port 5000), and a Jupyter Lab instance (on port 8888).
4. Run the data generation workflow via the REST API so that it produces the final training dataset at `/home/user/workspace/training_data.h5`.

Ensure your C++ binary writes strictly the two space-separated floating point numbers (average x, average y) to stdout, as it will be rigorously tested against an oracle with random inputs.