A researcher left behind a distributed numerical simulation pipeline under `/home/user/app/`, but it's currently broken. The pipeline consists of three services:
1. An HTTP API Gateway (Python/Flask) that receives raw observational data.
2. A Simulation Worker that takes the data, reshapes it using a Bash script, and runs an MPI-based numerical integrator (Python + mpi4py).
3. A simple TCP Results Aggregator that collects the final output.

Currently, the pipeline fails for several reasons:
- The services are not correctly pointing to each other's ports.
- The `reshape_data.sh` script incorrectly formats the observational data, causing the MPI simulator to read the wrong initial conditions.
- The MPI simulation environment is missing the correct library paths, and it is using a hardcoded time-step ($\Delta t = 1.0$) which causes the numerical integrator (a simple Euler method solving a decay equation) to diverge.
- The simulation worker's wrapper script `run_mpi_sim.sh` does not correctly invoke `mpirun` with the right number of processes (it should use 4 processes).

Your tasks are:
1. Examine the `docker-compose.yml` (or in this case, the `start_services.sh` script) and configuration files in `/home/user/app/config/`. Reconfigure them so the API Gateway listens on `127.0.0.1:8080`, talks to the Simulation Worker on port `5000`, and the worker sends results to the Aggregator on port `9090`.
2. Fix `/home/user/app/scripts/reshape_data.sh`. It currently receives comma-separated data `time,value,error` but the MPI script expects space-separated `time value`. Filter out any lines where `error` > 0.5.
3. Edit `/home/user/app/scripts/run_mpi_sim.sh` to correctly load the virtual environment `/home/user/venv` and run `mpirun -n 4 python simulator.py`.
4. Modify `simulator.py` to use a step-size of `dt = 0.01` instead of `1.0` to prevent divergence.

Ensure all services are running and correctly integrated. You can start the services by running `/home/user/app/start_services.sh`. Do not change the overall architecture, just fix the configuration and scripts.

When you are done, an automated verifier will send an HTTP POST request to `127.0.0.1:8080/simulate` with a CSV payload and will expect to retrieve the stabilized, integrated output from the Aggregator at `127.0.0.1:9090`. Leave the services running!