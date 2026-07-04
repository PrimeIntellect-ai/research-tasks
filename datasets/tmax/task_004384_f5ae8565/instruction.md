You are a bioinformatics analyst tasked with modeling the population growth of several pathogen variants based on their genetic sequences. 

You have been provided with an environment that contains a partially configured multi-service application under `/app/`. The application consists of a Redis database and a Python Flask web API, but they are not properly connected.

Your objectives are:

1. **Service Configuration & Startup**:
   - The Python API is located at `/app/api/app.py`. It currently fails to connect to Redis because it is configured to use the wrong port. Modify it to connect to Redis on the standard port `6379`.
   - Start the Redis server (a configuration file is available at `/app/redis/redis.conf`, or you can start it with default settings on port 6379).
   - Start the Python API so it listens on `0.0.0.0:8080`. (You may use the provided `/app/start.sh` script if you fix it, or start the services manually in the background).

2. **Sequence Processing and ODE Numerical Integration (Bash/Awk)**:
   - You have a FASTA file at `/home/user/sequences.fasta`.
   - Write a Bash script at `/home/user/process.sh` that parses this FASTA file.
   - For each sequence, calculate the GC content ratio, `r`, where `r = (number of G and C bases) / (total sequence length)`.
   - Use `r` as the growth rate in a logistic growth ordinary differential equation (ODE):
     `dP/dt = r * P * (1 - P / 100)`
   - Simulate this ODE numerically using **Euler's method** with a time step of `dt = 1` for `10` steps (from `t=0` to `t=10`).
   - The initial population at `t=0` is `P = 10.0`.
   - Perform these calculations using Bash commands (like `awk`, `bc`, etc.).

3. **Data Ingestion**:
   - For each sequence, after calculating the final population `P` at `t=10`, push this value to the Redis server.
   - The Redis key must be the sequence ID (e.g., `seq1`, excluding the `>`), and the value should be the final population `P`.

4. **Verification**:
   - Once your script finishes running, the API must be able to serve the results.
   - If an automated test queries `http://127.0.0.1:8080/api/population?seq_id=seq1`, it should return a JSON response with the calculated population rounded to two decimal places (handled by the API, provided you stored an accurate float in Redis).

Constraints:
- Do not modify the FASTA file.
- Do not rewrite the Python API in another language; just fix the Redis connection port.
- Your data processing and ODE solving script `/home/user/process.sh` must be primarily written in Bash (using standard Unix tools like `awk`, `sed`, `grep`, `bc`).