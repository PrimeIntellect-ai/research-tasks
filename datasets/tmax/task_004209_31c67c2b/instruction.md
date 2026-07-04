You are a data scientist troubleshooting a local bioinformatics modeling pipeline that recently broke. The pipeline analyzes k-mer profiles of GC-rich genetic sequences, fits a multivariate statistical model, and uses the model to identify target sequences for primer design. 

The pipeline consists of multiple cooperating services located in `/home/user/workspace/pipeline`:
1. A Sequence API (Flask) running on port `8050`.
2. A Redis cache for storing k-mer profiles.
3. The main modeling script: `fit_model.py`.

Currently, the pipeline is failing for two reasons:
1. **Service Misconfiguration:** The services are not communicating correctly. You need to adjust the configuration files (`config.yaml` and `redis.conf`) so that the Sequence API connects to the Redis cache, and `fit_model.py` can fetch data from the API and Cache. 
2. **Numerical Instability:** Once connected, `fit_model.py` crashes with a `LinAlgError`. The GC-rich nature of the sequences results in highly collinear k-mer frequencies, making the covariance matrix near-singular. 

Your tasks are to:
1. Start the Redis cache and Flask API in the background. Note: run Redis with the provided `redis.conf`. The Flask API is in `api.py`.
2. Fix the service configurations so `fit_model.py` can complete its data fetching phase.
3. Fix the numerical instability in `fit_model.py`. Modify the code to add a ridge penalty (Tikhonov regularization) of exactly $\lambda = 10^{-5}$ (i.e., $10^{-5} \times I$) to the covariance matrix BEFORE performing the Cholesky decomposition.
4. Calculate the 1-Wasserstein distance between the diagonal of the stabilized Cholesky lower-triangular matrix $L$ and a reference distribution provided in `/home/user/workspace/pipeline/reference_dist.npy`. Use `scipy.stats.wasserstein_distance`.
5. Identify the sequence ID that is closest to the reference distribution (lowest Wasserstein distance).
6. For that specific sequence, find the best 20-bp forward primer by finding the highest scoring local alignment (Smith-Waterman) against the target motif: `ATGCGTACGTAGCTAGCTAG`. Use match score = 2, mismatch penalty = -1, gap penalty = -2. 
7. Output your final results to `/home/user/workspace/pipeline/results.json` in the following exact format:
```json
{
    "best_seq_id": "string",
    "wasserstein_distance": float,
    "primer_sequence": "string"
}
```

Do not use root privileges. All files are in `/home/user/workspace/pipeline`.