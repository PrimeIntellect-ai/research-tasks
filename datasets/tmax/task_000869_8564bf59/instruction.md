You are acting as a bioinformatics analyst working on a spatial transcriptomics pipeline. We have a distributed system located in `/app/spatial_pipeline` that calculates morphogen concentration gradients based on sequence traits. 

The pipeline consists of three services that must be glued together:
1. A Redis database (stores sequence metadata and diffusion coefficients).
2. A Python Flask API (`/app/spatial_pipeline/api/app.py`) that acts as the orchestrator.
3. A C++ computational worker (`/app/spatial_pipeline/worker/pde_worker.cpp`) that solves a 1D Reaction-Diffusion PDE and performs Singular Value Decomposition (SVD) to extract the dominant spatial mode.

Currently, the pipeline is broken in several ways:
1. **Service Configuration:** The services are not communicating. You need to configure the `docker-compose.yml` (or run them manually/via a script) so that the Flask API listens on port 8080, connects to Redis on port 6379, and correctly invokes the compiled C++ worker via the command line.
2. **Numerical Instability:** The C++ worker diverges for high diffusion coefficients. The Explicit Euler scheme used for the PDE solver does not enforce the Courant-Friedrichs-Lewy (CFL) stability condition. You must modify `pde_worker.cpp` to adapt the time step `dt` dynamically based on the grid spacing `dx` and diffusion coefficient `D` to guarantee stability (e.g., `dt <= (dx * dx) / (2.0 * D)`).
3. **Matrix Decomposition:** The worker uses a basic SVD library to extract the dominant spatial mode of the concentration history matrix, but the extraction is flawed. Fix the SVD call to correctly output the 1st left singular vector.

Your task:
1. Fix the C++ source code in `/app/spatial_pipeline/worker/pde_worker.cpp`. You must ensure it uses OpenMP for parallelizing the spatial loop.
2. Compile the worker: `g++ -O3 -fopenmp pde_worker.cpp -o pde_worker -I/usr/include/eigen3`.
3. Fix the service configurations so the Python API can talk to Redis and execute the worker.
4. Start the services.
5. Trigger an end-to-end run by sending a POST request to `http://localhost:8080/analyze` with JSON payload `{"sequence_id": "SEQ_99", "time_end": 10.0}`.
6. The API should return a success message, and the pipeline should generate an output file at `/home/user/output_mode_SEQ_99.txt` containing the comma-separated dominant spatial mode vector.

Ensure the final numerical error of the spatial mode is minimal. We will verify your output against an analytical analytical solution threshold.