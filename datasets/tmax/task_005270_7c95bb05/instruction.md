You are a bioinformatics analyst setting up an automated sequence processing pipeline. Your task involves fixing a broken microservice architecture and writing an anomaly detection script to filter out adversarial sequencing data.

### Part 1: Service Composition
Our ingestion pipeline has three cooperating services that are started via a script (`/home/user/start_services.sh`), but they are currently misconfigured and failing to communicate.
1. **Nginx Reverse Proxy:** Should listen on port 8080. It needs to route requests starting with `/api/upload` to the Ingestion API, and `/api/align` to the Alignment Worker.
2. **Ingestion API (Flask):** Runs locally on port 5000. It receives uploaded HDF5 files and pushes them to Redis.
3. **Alignment Worker (FastAPI):** Runs locally on port 5001. It pulls from Redis and aligns sequences.
4. **Redis:** Runs locally on port 6379.

**Your goal for Part 1:** 
Fix the configuration files so the end-to-end flow works. When functioning correctly, a POST request to `http://localhost:8080/api/upload` with an HDF5 payload should successfully queue the sequence, and a GET to `http://localhost:8080/api/align/status` should return `{"status": "listening"}`.
- Fix `/home/user/config/nginx.conf` so it correctly maps the routes.
- Fix `/home/user/config/.env` so the Ingestion API and Alignment Worker point to the correct Redis port (they are currently pointing to a non-existent port 6380).

### Part 2: Adversarial Sequence Filter
The pipeline occasionally receives "poisoned" sequencing runs (evil data) designed to crash the SVD-based sequence alignment algorithms. 
You must write a Python classifier at `/home/user/filter.py` that reads an HDF5 file, analyzes the sequence, and determines if it is valid or malicious.

**Technical Specifications for `filter.py`:**
- Accepts exactly one CLI argument: the path to an HDF5 file.
- The HDF5 file contains a dataset named `/quality_scores` (a 2D matrix of floats representing sequence quality correlations).
- **Detection Logic:** You must perform a Singular Value Decomposition (SVD) on the `/quality_scores` matrix. Real biological sequences (clean) have a structured quality distribution, typically resulting in the largest singular value being **less than 10.0**. Adversarial/poisoned sequences (evil) have artificially flattened distributions, resulting in the largest singular value being **greater than 15.0**.
- The script must print exactly `ACCEPT` to stdout if the file is clean, and `REJECT` if the file is malicious. It should exit with code 0 in both cases.

There are two directories containing sample test data:
- `/home/user/data/clean/` (contains clean `.h5` files)
- `/home/user/data/evil/` (contains poisoned `.h5` files)

You must ensure your script correctly classifies all files in these directories, as the automated test will evaluate your script against identical, hidden corpora. Ensure all services are running and correctly configured by the end of your session.