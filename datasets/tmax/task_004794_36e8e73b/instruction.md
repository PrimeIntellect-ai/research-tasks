As a Machine Learning Engineer, you are tasked with preparing a training dataset of target distributions derived from covariance matrices. Unfortunately, our standard matrix factorization pipeline fails because some of the input matrices are near-singular.

We have a proprietary legacy binary that robustly handles these near-singular matrices and outputs the correct target probability distribution. You must build a C++ data preparation service that interfaces with this binary and serves a distance metric for our training loop.

**Your objectives:**

1. **Process the HDF5 Data:** 
   Read `/app/raw_data.h5`. It contains a single dataset named `covariances` with shape `(50, 10, 10)` (50 matrices of size 10x10, stored as 64-bit floats). 
   *(Note: You may need to install HDF5 development libraries).*

2. **Query the Oracle:**
   For each of the 50 matrices, invoke the stripped legacy binary located at `/app/oracle_dist`. 
   - The binary expects exactly 100 space-separated floats on `stdin` (row-major order of the 10x10 matrix).
   - It prints exactly 10 space-separated floats to `stdout`, representing the target probability distribution $P$ (which sums to 1).

3. **Serve the Data Preparation API:**
   Write and run a C++ HTTP server listening exactly on `127.0.0.1:9000`. You may use single-header libraries like `cpp-httplib` (which you can download using wget) and `nlohmann/json`.
   
   The server must implement the following endpoint:
   - **Method:** `POST /metric`
   - **Authentication:** Must require an HTTP header `Authorization: Bearer secret-ml-token-99`
   - **Request Body (JSON):** 
     ```json
     {
       "index": 5,
       "candidate": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
     }
     ```
     `index` is the 0-based index of the matrix (0 to 49). `candidate` is a 10-element probability distribution $Q$ proposed by our training loop.
   - **Computation:** Calculate the Kullback-Leibler (KL) divergence $D_{KL}(P || Q) = \sum_{i} P_i \log(P_i / Q_i)$, where $P$ is the distribution obtained from the oracle for the given `index`, and $Q$ is the `candidate` distribution. (Add $10^{-9}$ to denominators and log arguments to prevent NaN/Inf if necessary).
   - **Response Body (JSON):**
     ```json
     {
       "distance": 0.45321
     }
     ```
     *(Respond with HTTP 200 on success, 401 for bad auth, 400 for bad input).*

Keep this server running in the background. Once the server is online and successfully listening on port 9000, create an empty file at `/tmp/server_ready` to signal that verification can begin.