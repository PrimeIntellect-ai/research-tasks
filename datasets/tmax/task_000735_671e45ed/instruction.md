You are a bioinformatics analyst working with Monte Carlo simulated mass-spectrometry data of protein sequences. 

Your organization uses a proprietary (vendored) Python package called `biomatrix` to perform matrix decompositions on this signal data. However, the latest batch of simulated data contains near-singular matrices, which causes `biomatrix` to crash with a `LinAlgError`.

Your task is to fix the vendored package, process the data, and expose the results via a simple web service.

Step 1: Fix the Vendored Package
The source code for `biomatrix` version 0.1.0 is located at `/app/vendor/biomatrix-0.1.0`. 
Inside this package, the module `biomatrix/solver.py` contains a function `factorize_signal(matrix)`. It currently attempts a direct Cholesky decomposition. You must modify this function to add a Tikhonov regularization term of `1e-5` (i.e., add `1e-5` to the diagonal of the matrix before decomposition) to handle near-singular inputs gracefully. After fixing it, install the package in the current environment.

Step 2: Process the Data
An HDF5 file containing the simulated sequence spectra is located at `/app/data/spectra.h5`. The file contains a root group with datasets named `seq_0`, `seq_1`, ..., `seq_49`. Each dataset is a 2D matrix representing the signal.
Write a Bash script (and accompanying Python code if necessary) to load each dataset, process it using the fixed `biomatrix.solver.factorize_signal`, and extract the trace (sum of the diagonal elements) of the resulting lower-triangular matrix $L$. Save these results to `/home/user/results.txt` in the format `seq_N: <trace>`.

Step 3: Expose the Results via a Network Service
Launch an HTTP server listening on `127.0.0.1:9090`. 
The server must implement the following protocol:
- It must accept `GET` requests to the endpoint `/trace/<seq_id>` (e.g., `/trace/seq_5`).
- It must require an Authorization header: `Authorization: Bearer secret-bio-token`.
- If the token is valid, it should return the calculated trace for that sequence as plain text (e.g., `12.4502`).
- If the token is missing or invalid, it must return a `401 Unauthorized` status.

Write a master Bash script at `/home/user/run_pipeline.sh` that automates this entire process (installs the fixed package, runs the processing, and starts the server in the background). Leave the server running.