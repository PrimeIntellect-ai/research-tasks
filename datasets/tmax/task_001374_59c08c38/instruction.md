You are acting as a data scientist configuring a model validation pipeline. We have a pre-packaged validation server vendored at `/app/protein-model-server` that exposes an HTTP API to compare experimental protein data against an analytical model.

Your task is to fix the vendored package, start the server, and ensure it correctly serves the required endpoint.

**System State and Data:**
1. A FASTA file at `/app/data/proteins.fasta` containing protein sequences.
2. An HDF5 file at `/app/data/experiments.h5` containing experimental validation curves (arrays of floats) for each protein at the dataset path `/experiments/{id}/curve`.
3. The vendored server package at `/app/protein-model-server/`. It contains a Python HTTP server (`server.py`) and a data extraction shell script (`compute.sh`). 

**API Requirements:**
- The server must listen on `127.0.0.1:8080`.
- It must handle `GET /api/protein/{id}/validate`.
- It must require an `Authorization: Bearer protein-secret-42` header. Requests missing this exact token must return a `401 Unauthorized` status.
- For valid requests, it should return a `200 OK` status with a JSON payload: `{"id": "{id}", "length": L, "mse": <mse_value>}`.

**Analytical Model & Logic:**
When the endpoint is queried for a specific `{id}`:
1. Find the sequence for `{id}` in the FASTA file. Calculate its length, $L$ (number of amino acid characters, ignoring newlines and the header).
2. Extract the experimental curve array for `{id}` from the HDF5 file. Let the number of points in this array be $N$.
3. Compute the analytical model curve for $t = 0, 1, \dots, N-1$ using the formula:  
   $y_t = L \cdot (1 - e^{-0.05 \cdot t})$
4. Calculate the Mean Squared Error (MSE) between the analytical curve and the experimental curve.
5. The `mse` value in the JSON response should be rounded to exactly 2 decimal places.

**The Perturbation:**
The vendored package is broken:
- The server is misconfigured to listen on the wrong port.
- The `compute.sh` script has logic errors in how it parses the FASTA file and extracts data from the HDF5 file using `h5dump`.
- The analytical formula in the script has a mathematical error.

**Instructions:**
1. Inspect the data files in `/app/data/` to understand their structure.
2. Fix the files in `/app/protein-model-server/` so that it correctly implements the API and math logic.
3. Start the server in the background so it is actively listening on `127.0.0.1:8080`.
4. Create a log file at `/home/user/server_started.log` containing the exact PID of the running server process to indicate you are finished.

You may use standard CLI tools, Bash, and Python 3 (with standard libraries plus `h5py` if you prefer).