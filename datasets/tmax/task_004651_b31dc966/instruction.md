You are tasked with fixing a scientific computation pipeline that keeps crashing due to ill-conditioned input data. 

The system consists of three services running locally:
1. A Redis message broker (port 6379).
2. A Flask API Gateway (port 5000) located at `/app/api/app.py`, which receives HDF5 file uploads, saves them to `/tmp/uploads/`, and pushes the file path to a Redis queue.
3. A Compute Worker located at `/app/worker/worker.py`, which pops file paths from Redis, loads the HDF5 file, and performs a matrix-based curve fitting using least squares (`np.linalg.inv(X.T @ X)`).

Currently, when users upload HDF5 files where the dataset `matrix_X` is near-singular, the Compute Worker crashes with a `LinAlgError`.

Your goal is to build a detector and integrate it into the API:
1. **Create a detector**: Write a Python script at `/home/user/detector.py` that takes a single command-line argument (the path to an HDF5 file). It must read the dataset named `matrix_X` from the file. If the condition number of `matrix_X.T @ matrix_X` is strictly less than $10^5$, it should print `CLEAN` to standard output. If it is greater than or equal to $10^5$ (or if it's completely singular), it should print `EVIL`.
2. **Integrate and reconfigure**: Modify the Flask API in `/app/api/app.py` so that, upon receiving an upload, it first saves the file, then runs `/home/user/detector.py` via a subprocess. 
    - If the detector outputs `CLEAN`, push to Redis and return HTTP 200.
    - If the detector outputs `EVIL`, delete the file, DO NOT push to Redis, and return HTTP 400.
3. Restart the Flask service so your changes take effect. You can manage the services using the provided `/app/start_services.sh` and `/app/stop_services.sh` scripts.

To help you test your detector, we have provided sample reference datasets in `/app/corpora/clean/` (which should all be flagged as CLEAN) and `/app/corpora/evil/` (which should all be flagged as EVIL).