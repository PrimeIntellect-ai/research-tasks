You are a bioinformatics analyst tasked with deploying a local sequence analysis microservice. 

We rely on a local package called `seqtools` vendored at `/app/seqtools`. This package is used to score the stability of DNA sequences using a k-mer profiling algorithm. However, a recent commit broke the package, and it currently fails when scoring sequences due to a matrix dimension mismatch in `/app/seqtools/scorer.py`.

Your task:
1. Fix the `seqtools` package. The `WEIGHT_MATRIX` in `/app/seqtools/scorer.py` was accidentally truncated. It should be a 4x4 identity matrix (representing A, C, G, T), but it is currently a 3x4 matrix. Correct it to a 4x4 identity matrix (`[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]`).
2. Write a Python HTTP service using the standard `http.server` library (or any framework you prefer, but no internet is available to pip install new things) that listens on `127.0.0.1:8080`.
3. The service must expose a `POST /analyze` endpoint. It will receive a JSON payload like `{"sequence": "ATGCATGCATGC"}`.
4. For the given sequence, use `seqtools.scorer.score_profile(sequence)` to get a 1D numpy array of stability scores.
5. Calculate the numerical derivative of this score array using `numpy.gradient`.
6. Return a JSON response containing the derivative values as a list of floats: `{"derivative": [0.0, 0.5, ...]}`.
7. Start the server as a background process so it is running when we verify. Save the server script at `/home/user/server.py`.

No external internet access is provided. Use standard library modules and `numpy` (which is pre-installed).

Start the server and leave it running on `127.0.0.1:8080`.