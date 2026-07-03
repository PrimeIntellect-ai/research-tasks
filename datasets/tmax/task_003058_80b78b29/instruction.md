You are a bioinformatics analyst tasked with building a sequence filtering pipeline. We receive DNA sequences, some of which are synthetic/anomalous ("evil") and some of which are natural ("clean"). We have a local set of microservices that compute a statistical "naturalness" score for a given sequence using Matrix Decomposition (SVD on k-mer frequencies) and MCMC sampling to estimate the posterior probability of it being natural.

However, the pipeline is currently broken, and we need you to fix the infrastructure and write the bash orchestration tool.

### Part 1: Service Configuration (Multi-Service)
We have three services located in `/app/services/`:
1. **Redis**: Cache for MCMC transition matrices. (Should run on `127.0.0.1:6379`)
2. **Scoring API (Flask)**: Found in `/app/services/api/`. It calculates the statistical convergence and scores. It is currently failing to connect to Redis, and its binding port is misconfigured.
3. **Nginx**: Found in `/app/services/nginx/`. It acts as a reverse proxy on port `8080` to the Flask API. Its configuration `nginx.conf` has the wrong upstream backend.

Your task:
- Fix the configurations so Nginx listens on `8080`, proxies to the Flask API, which successfully connects to Redis.
- Start all three services in the background. (Use `redis-server`, `python3 app.py`, and `nginx -c /app/services/nginx/nginx.conf`).

### Part 2: Bash Classifier
Write a Bash script at `/home/user/sequence_classifier.sh` with the following signature:
`bash /home/user/sequence_classifier.sh <input_directory> <output_directory>`

For every `.fasta` file in the `<input_directory>`:
1. Extract the sequence (ignore the `>` header line, concatenate multi-line sequences).
2. Query the Nginx endpoint: `POST http://127.0.0.1:8080/score` with JSON payload `{"sequence": "<sequence_string>"}`.
3. The API will return a JSON response: `{"score": <float>, "converged": <boolean>}`.
4. If `converged` is true AND `score >= 0.5`, the sequence is "clean". Copy the original `.fasta` file to the `<output_directory>`.
5. If it is "evil" (score < 0.5 or failed convergence), DO NOT copy it to the output directory. Instead, append its filename to `/home/user/rejected.log`.

### Part 3: Execution
We have provided two corpora of `.fasta` files for you to test against:
- Evil corpus: `/app/data/evil/`
- Clean corpus: `/app/data/clean/`

Run your script against both directories (e.g., outputting clean sequences to `/home/user/clean_out/` and `/home/user/evil_out/`). To succeed, your solution must completely preserve the clean corpus and completely reject the evil corpus.

Ensure your Bash script is executable and robust.