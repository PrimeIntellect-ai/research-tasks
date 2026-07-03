You are tasked with building a C++ data processing tool and fixing a broken ETL pipeline for a data analyst. 

The pipeline consists of multiple cooperating services located in `/app/services/`:
1. A Redis instance serving as our experiment tracking and configuration store.
2. A Python Flask service (acting as a configuration provider) that reads a correlation threshold from Redis and serves it via an HTTP GET request.

Currently, the services are misconfigured. The data analyst reported that the system produces errors when attempting to run the pipeline.

Your objectives:
1. **Fix the multi-service pipeline**: 
   - Inspect the configuration files in `/app/services/flask_service/` and the startup script `/app/start_services.sh`.
   - Reconfigure the services so that the Flask app successfully connects to the Redis instance and serves the threshold value on `http://127.0.0.1:5000/threshold`. 
   - You must initialize the Redis key `threshold` to `0.85` so the Flask app can serve it.
   - Run `/app/start_services.sh` to ensure everything is up.

2. **Build the C++ Data Filter (`/home/user/csv_filter`)**:
   - Write a C++ program (`/home/user/csv_filter.cpp`) and compile it to `/home/user/csv_filter`.
   - The program should take a single argument: the path to a CSV file.
   - The CSV files have headers: `id,val_X,val_Y,val_Z`.
   - **Tokenization & ETL**: Parse the CSV file and extract the numerical columns `val_X` and `val_Y`.
   - **Correlation & Linear Algebra**: Compute the Pearson correlation coefficient ($r$) between `val_X` and `val_Y`. You must compute the means, variances, and covariance manually to derive this.
   - Fetch the dynamic threshold from `http://127.0.0.1:5000/threshold`.
   - **Experiment Tracking**: If the absolute value of the correlation $|r|$ is strictly greater than the threshold fetched from the API, the file is considered an adversarial anomaly ("evil"). Otherwise, it is "clean". 
   - The program must append the string `<filename>: EVIL` or `<filename>: CLEAN` to a file `/home/user/experiment_log.txt`.
   - The program MUST exit with code `1` if the file is EVIL, and exit with code `0` if the file is CLEAN.

We have provided two directories containing datasets:
- `/app/corpus/clean/` (Contains normal CSV files)
- `/app/corpus/evil/` (Contains CSV files with artificially injected high-correlation noise)

Your C++ program must correctly classify 100% of the files in both corpora. Compile your code using `g++` (you may use `libcurl` for the HTTP request). Ensure your final executable is located exactly at `/home/user/csv_filter`.