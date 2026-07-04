You are helping a researcher debug and deploy a local simulation pipeline that processes noisy spectroscopy data. The pipeline consists of a data server and a processing API. The setup is currently broken, and you need to fix the processing service, manage its scientific environment, and ensure the services communicate properly.

Your tasks:
1. **Environment Setup**: 
   Create a Python virtual environment at `/home/user/venv` and install the necessary scientific and web libraries (`numpy`, `h5py`, `flask`, `requests`, `scipy`).
   Modify the provided `/app/startup.sh` script to activate this virtual environment before starting the services.

2. **Fix the Processing API** (`/app/processor_api.py`):
   The data server runs on `http://127.0.0.1:8081` and serves an HDF5 file at the `/data` endpoint.
   You must implement the `/solve` endpoint in `/app/processor_api.py` (which runs on port 8082). When `GET /solve` is requested, the API must:
   - Download the HDF5 file from `http://127.0.0.1:8081/data` and save it temporarily.
   - Read the dataset `spectroscopy/raw` (a 2D matrix $M$) and `spectroscopy/vector` (a 1D array $b$) from the HDF5 file.
   - Perform Singular Value Decomposition (SVD) on $M$.
   - Reconstruct the matrix $M_{filtered}$ using ONLY the top 3 largest singular values (set the rest to zero).
   - Solve the linear equation $M_{filtered} \cdot x = b$ for $x$ using ordinary least squares (`numpy.linalg.lstsq` or equivalent).
   - Return the resulting vector $x$ as a JSON list of floats.

3. **Service Composition**:
   Ensure both `/app/data_server.py` (on port 8081) and `/app/processor_api.py` (on port 8082) are started correctly by `/app/startup.sh`. The startup script should run them in the background so the script exits gracefully while leaving the services running.

Run `/app/startup.sh` once you have completed the fixes. We will verify your work by making a protocol-level HTTP GET request to `http://127.0.0.1:8082/solve` and checking the returned JSON array against the mathematically exact solution.