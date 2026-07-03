You are a data engineer debugging and rebuilding a legacy ETL pipeline. 

We have a legacy compiled binary located at `/app/analyzer`. This binary is supposed to read a comma-separated list of 5 floating-point numbers from standard input, perform a linear algebra projection (similarity search algorithm), and print a single floating-point anomaly score to standard output. 

Currently, our pipeline is broken. Whenever we pipe data to `/app/analyzer`, it simply produces blank output. This resembles a known misconfiguration issue where the computational backend is not specified. Through historical logs, we know it requires a specific environment variable to function properly, but the exact variable name is lost. You will need to inspect or reverse-engineer the binary to figure out how to make it output the computed scores instead of blank lines.

Your task is to build a new microservice to replace the broken pipeline. You may use Python, Bash, or any combination of standard CLI tools. 

Requirements for your service:
1. **HTTP Server**: Create and run an HTTP server listening exactly on `127.0.0.1:5050`.
2. **Authentication**: The server must reject any requests that do not contain the header `X-Pipeline-Token: alpha-etl-883`.
3. **Endpoint**: It must accept HTTP POST requests to the `/process` endpoint. The POST body will be a raw CSV string containing exactly 5 values (e.g., `1.2,3.4,?,5.5,1.0`).
4. **Imputation**: The incoming data may contain `?` characters representing missing values. Your service must dynamically compute the column mean for any missing feature using the historical dataset provided at `/home/user/reference_data.csv`. The `?` should be replaced with this computed mean before passing the data to the binary.
5. **Execution**: Pass the imputed comma-separated string to `/app/analyzer` via stdin, ensuring the environment is configured so it doesn't output blank lines.
6. **Response**: The HTTP response must be a JSON object containing the imputed data and the resulting score: `{"imputed": [1.2, 3.4, 2.1, 5.5, 1.0], "score": 14.52}`.

The historical dataset `/home/user/reference_data.csv` contains 100 rows of valid 5-column float data. 
Ensure your service is running in the background and listening on the port before you complete the task. Write your service code in `/home/user/etl_service.py` (or `.sh`) and leave it running.