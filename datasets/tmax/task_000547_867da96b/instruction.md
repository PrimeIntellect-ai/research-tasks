I need help setting up a distributed simulation environment for my research. We are simulating a 1D heat equation across a decomposed mesh, and I need to orchestrate the services, implement the domain decomposition, and verify the results against a reference dataset.

Here is the setup in `/app/sim_env/`:
- `coordinator.py`: A Flask application that should run on port 5000. It coordinates the simulation. I have left the `split_mesh(N, k)` function empty. You need to implement it. It should take a total grid size `N` and number of workers `k`, and return a list of tuples `(start_idx, end_idx)` representing the subdomain indices for each worker, dividing the grid as evenly as possible. If `N` is not perfectly divisible by `k`, distribute the remainder by adding 1 to the size of the first `N % k` subdomains.
- `worker.py`: A worker script that expects a POST request on its `/compute` endpoint with JSON `{"start": x, "end": y}`. We need two workers running on ports 5001 and 5002.
- `data_server.py`: Serves the reference dataset at `http://127.0.0.1:8080/reference.json`.
- `docker-compose.yml` (or similar startup script `start_services.sh`): You need to create a bash script `/home/user/start_services.sh` that starts the data server on 8080, coordinator on 5000, and two workers on 5001 and 5002. All logs should be redirected to `/home/user/service_logs/`.

Additionally, I need you to write a regression test script at `/home/user/regression_test.py`. This script must:
1. Send a POST request to the coordinator at `http://127.0.0.1:5000/run_sim` with JSON `{"N": 100, "workers": 2}`. The coordinator will split the mesh and query the workers, returning a combined JSON array of the simulation results.
2. Fetch the reference dataset from `http://127.0.0.1:8080/reference.json`.
3. Compare the coordinator's result array with the reference array.
4. Print "REGRESSION_PASSED" to standard output if the maximum absolute difference between any corresponding elements is less than 1e-5. Otherwise, print "REGRESSION_FAILED".

Please fix `coordinator.py`, create `start_services.sh` to glue everything together, and write the regression test script. Make sure `start_services.sh` is executable and run it so the services are listening. Let me know when the setup is running and the test script is ready!