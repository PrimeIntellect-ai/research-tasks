You are acting as a bioinformatics analyst. We are migrating an old sequence analysis pipeline to a new microservice architecture. 

Your task has two main parts:

Part 1: Metric Implementation (Fuzz Equivalence)
We have a legacy compiled binary located at `/app/legacy_kmer_dist` which takes two DNA sequences as arguments and outputs a distance metric based on 3-mer distributions. 
You must write a Python script `/home/user/kmer_dist.py` that exactly replicates the mathematical behavior of this legacy binary. 
The legacy binary calculates the Euclidean distance between the L1-normalized 3-mer frequency distributions of the two sequences. 
- A 3-mer is any substring of length 3. There are 64 possible 3-mers (AAA to TTT).
- For a sequence, count the occurrences of all 64 overlapping 3-mers.
- Add a pseudocount of 1 to all 64 3-mer counts.
- Normalize the 64-dimensional vector so its sum is 1.0.
- Calculate the Euclidean distance between the two normalized vectors.
- Your script must accept two arguments (the two sequences) and print the distance as a standard float rounded to 6 decimal places.

Part 2: Multi-Service Architecture
Under `/app/services/` you will find three components:
1. `gateway/`: A Flask application that exposes a REST API on port 8000.
2. `worker/`: A Celery worker that processes background tasks.
3. `docker-compose.yml`: A compose file defining `gateway`, `worker`, and `redis`.

You need to:
1. Complete the Celery task in `/app/services/worker/tasks.py` to call your `/home/user/kmer_dist.py` script.
2. Fix the configuration in `/app/services/gateway/app.py` so it properly sends the task to Redis (running on the `redis` host at port 6379).
3. Start the services using `docker-compose up -d` (or by running the python processes manually if Docker is unavailable, simulating the compose environment). 
4. The gateway must be running on `127.0.0.1:8000`. When a POST request is made to `http://127.0.0.1:8000/analyze` with JSON `{"seq1": "ATCG...", "seq2": "CGTA..."}`, it must return a JSON response `{"distance": <float>}`.

Ensure your `kmer_dist.py` is perfectly accurate and handles sequences containing only A, C, G, and T.