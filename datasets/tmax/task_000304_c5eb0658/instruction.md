You are a data engineer tasked with fixing and completing an ETL pipeline that performs statistical transformations on time-series data. The pipeline consists of multiple services that need to be properly configured, and a core processing script that you must write from scratch.

### Part 1: Service Configuration
There is a multi-service pipeline located in `/app/`. At solve time, a startup script launches:
1. A Redis server
2. A Flask data API (`/app/data_api.py`)
3. An ETL orchestrator (`/app/orchestrator.py`)

Currently, they are misconfigured and cannot communicate. 
- The Flask API is trying to start on a restricted port. Reconfigure `/app/config/api.json` so the Flask app listens on port `8080`.
- The ETL orchestrator is trying to connect to a non-existent message broker. Update `/app/config/orchestrator.json` to point the `broker_url` to the local Redis instance on port `6379`.

### Part 2: ETL Processor Implementation
The orchestrator relies on a standalone data processing script to perform linear algebra transformations. You must create this script at `/home/user/processor.py`.

Requirements for `/home/user/processor.py`:
- It must read a JSON string from `stdin`. The JSON will have the format: `{"data": [[...], ...]}` representing an $N \times M$ matrix (N rows/samples, M columns/features).
- Compute the column-wise mean and mean-center the data (subtract the mean of each column from the respective column). Let this be $X_c$.
- Compute the sample covariance matrix $C$ of the features (size $M \times M$). Use $N-1$ for normalization (assume $N > 1$).
- Apply a linear transformation by multiplying the mean-centered data by the covariance matrix: $Y = X_c \times C$.
- Output the result to `stdout` as a valid JSON object: `{"covariance": [[...]], "transformed": [[...]]}`.
- To ensure pipeline reproducibility and bit-exact equivalence, round all floating-point numbers in the output JSON to exactly 4 decimal places before serialization.

Ensure `/home/user/processor.py` is executable (`chmod +x`). 
Your script will be tested against a reference oracle with hundreds of randomly generated matrices to ensure mathematical correctness and formatting equivalence.