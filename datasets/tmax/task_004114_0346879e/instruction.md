You are acting as a bioinformatics analyst. We need you to build a small sequence scoring API. 

Here are the requirements:

1. **Compile and Install Vendored Package:**
   We have vendored a proprietary C-extension package called `seq_scorer` located at `/app/vendored/seq_scorer-1.0.0`. However, the build is currently failing due to a deliberate misconfiguration in its `setup.py`. You must identify the compilation error, patch the `setup.py` file, and successfully install the package into the current Python environment. 

2. **Process Observational Data:**
   We have observational sequence data stored in an HDF5 file at `/app/data/observational.h5`. The file contains a single HDF5 dataset named `reads` under the root group, consisting of string DNA sequences.
   - Read these sequences.
   - Use the `seq_scorer.score_sequence(seq)` function (from the package you just installed) to compute the score for each read.
   - Compute the mean score of these reads.

3. **Bootstrap Confidence Intervals & Reference Comparison:**
   - Using 10,000 bootstrap resamples (with replacement) of the scores computed above, calculate the 95% confidence interval for the *mean score* using the percentile method. 
   - Use a random seed of `42` (e.g., `numpy.random.seed(42)` or `random.seed(42)`) before generating your bootstrap resamples so the results are deterministic.
   - We compare this against a known reference mean. Sequences are considered "anomalous" if their individual score falls strictly outside the 95% confidence interval of the mean.

4. **Expose an API:**
   Write and run a Python HTTP server (e.g., using Flask, FastAPI, or `http.server`) that listens on `127.0.0.1:8080`. The API must support two endpoints:
   - `GET /ci`
     Returns a JSON object with the computed statistics:
     `{"mean": <float>, "ci_lower": <float>, "ci_upper": <float>}`
   - `POST /score`
     Accepts a JSON payload `{"sequence": "<DNA string>"}` and returns:
     `{"score": <float>, "is_anomalous": <boolean>}`
     The `score` is calculated using `seq_scorer.score_sequence()`, and `is_anomalous` is `true` if the score is strictly less than `ci_lower` or strictly greater than `ci_upper`.

The server must remain running in the foreground or background so that our automated verifier can test it.