You are acting as a bioinformatics analyst. We have a locally running system consisting of multiple services that handle sequence processing and storage. Your goal is to write a Bash orchestration script that retrieves data, processes sequence alignments, calculates distribution distances, and numerically integrates sequence metrics.

System Context:
There is a sequence metadata API running on `127.0.0.1:8000` and a Redis caching server on `127.0.0.1:6379`. 
The API has an endpoint `http://127.0.0.1:8000/api/v1/sequences` which returns a list of sequence IDs in JSON format.
For each sequence ID, you can download an HDF5 container containing the raw reads and primer metadata at `http://127.0.0.1:8000/api/v1/download/<seq_id>`.

Your objective is to write a Bash script located at `/home/user/process_pipeline.sh` that performs the following steps:
1. Reconfigure the local service connections: The sequence API is currently failing because it cannot reach the Redis cache. You must update the configuration file `/app/api/config.ini` to point to `localhost:6379` instead of `redis-db:6379` and restart the API service (running as a background python process from `/app/api/server.py`).
2. Fetch the list of sequence IDs.
3. For each sequence, download the corresponding HDF5 file.
4. Use `h5dump` (installed on the system) to extract the "kmer_frequencies" array and the "melting_curve" array from the HDF5 file.
5. Calculate the Manhattan distance between the sequence's k-mer frequency distribution and a reference distribution (which is uniform across 16 k-mers, i.e., 0.0625 for each).
6. Perform a simple numerical integration (using the Trapezoidal rule) over the "melting_curve" array data points (which are given at 1-degree Celsius intervals) to calculate the total binding energy integral.
7. Combine these metrics to calculate a final "Alignment Score" for each sequence: `Score = (Integration_Result) / (Manhattan_Distance + 1)`.
8. Output a CSV file at `/home/user/candidate_scores.csv` with the format: `Sequence_ID,Alignment_Score`. The output should be sorted by Sequence_ID in ascending order.

Requirements:
- Only use Bash built-ins, coreutils, and standard tools (`curl`, `jq`, `h5dump`, `awk`, `bc`, `sed`).
- Ensure `/home/user/process_pipeline.sh` is executable.