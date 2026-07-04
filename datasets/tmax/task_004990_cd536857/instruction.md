You are a bioinformatics analyst working on a sequence processing pipeline. We are screening synthetic genetic constructs that control a metabolic pathway. 

Our system uses a multi-service architecture:
1. An `nginx` reverse proxy (listening on port 8080) that forwards requests to an API.
2. A Python `api_server` (listening on port 5000) that receives FASTA sequences via POST requests and pushes them to a job queue.
3. A `redis` server (listening on port 6379) for the job queue.
4. A Python `worker` process that pulls from Redis and executes a fast screening script (`/home/user/filter.sh`) to decide if a sequence should be accepted or rejected.

However, the system is currently broken and incomplete:
- The `nginx` configuration (`/app/nginx.conf`) is missing the correct upstream route to the `api_server`.
- The `worker` process environment variables in `/app/worker.env` are incorrectly configured and cannot connect to Redis.
- The fast screening script `/home/user/filter.sh` does not exist.

Your task has two parts:
1. **Fix the multi-service pipeline**: Correct the configuration files so that all services can communicate. Start the services (nginx, redis, api_server, worker).
2. **Develop the screening filter**: Some sequences are known to cause severe numerical instability (non-convergence) in our downstream ODE solver due to extreme melting temperatures. We have provided two directories of example sequences:
   - `/app/corpus/clean/` (sequences that are well-behaved)
   - `/app/corpus/evil/` (sequences that cause the ODE solver to crash)
   
   Analyze these corpora to determine the sequence properties that cause failure. Then, write a Bash script `/home/user/filter.sh` that takes a FASTA file path as its first argument. The script must evaluate the sequence and exit with code `0` if it is clean (safe), and exit with code `1` if it is evil (unstable). Your script should be fast and use standard Bash/Unix text processing tools (e.g., `grep`, `awk`, `sed`), without running the slow ODE solver.

**Requirements**:
- Fix `/app/nginx.conf` and `/app/worker.env`.
- Bring up the services so that a POST request to `http://localhost:8080/submit` with a fasta payload successfully processes the job.
- `/home/user/filter.sh` must correctly classify 100% of the provided clean and evil corpora.
- The automated test will verify your filter against a hidden hold-out dataset by submitting them through the `nginx` proxy.