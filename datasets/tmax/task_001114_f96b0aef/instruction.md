I have a legacy simulation pipeline that we use to model particle collision cross-sections. The core simulation is an old, stripped, compiled binary located at `/app/sim_binary`. We don't have the source code anymore. 

When you run `/app/sim_binary <mesh_size>`, it performs a domain decomposition and simulates the mesh, outputting an HDF5 file named `sim_output.h5` in the current working directory. The file contains a single 2D dataset named `/covariance_matrix`. 

Because of aggressive compiler optimizations and non-deterministic floating-point reduction order in the parallel mesh evaluation, the generated matrix has slight numerical noise that ruins our downstream statistical hypothesis tests.

To stabilize our analysis, I need you to build a multi-language REST wrapper around this simulation. 

Please create a web service (using Python, Node, or whatever you prefer) that:
1. Listens on `127.0.0.1:8080`.
2. Exposes an HTTP POST endpoint at `/run_sim`.
3. Accepts a JSON payload like this: `{"mesh_size": 256}`.
4. Executes the `/app/sim_binary` with the provided `mesh_size`.
5. Reads the resulting `/covariance_matrix` from `sim_output.h5`.
6. Performs Singular Value Decomposition (SVD) on the matrix to extract the dominant stable feature.
7. Returns a JSON response with the largest (top) singular value: `{"dominant_singular_value": <float>}`.

Leave the service running in the foreground or background so I can test it. Ensure it handles sequential requests gracefully and overwrites/cleans up the `sim_output.h5` file between runs.