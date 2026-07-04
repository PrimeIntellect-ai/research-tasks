You are an AI data scientist specializing in bioinformatics pipelines. Your goal is to debug a microservice data backend, extract primer sequence data, and write a Rust program to fit a predictive model for primer melting temperatures ($T_m$).

**Background**
We have a local data pipeline under `/app/` that provides training data for primer design. It consists of two services:
1. A Redis cache holding raw sequence metadata.
2. A Python API serving the sequences in FASTA format, annotated with experimentally determined $T_m$ values.

Currently, the pipeline is broken. A startup script (`/app/start_services.sh`) launches both services, but querying the API returns errors because the services are misconfigured and cannot communicate.

**Your Tasks:**
1. **Fix the Services:** Inspect the configuration files in `/app/api/` and `/app/redis/`. Identify why the Python API (running on port 8000) cannot communicate with the Redis instance. Fix the configuration, and ensure both services are running and integrated. You can restart them by re-running `/app/start_services.sh`. When correctly glued, `curl http://127.0.0.1:8000/dataset` will stream a FASTA file.

2. **Data Ingestion (Rust):** Create a new Rust project in `/home/user/primer_pipeline`. Write a Rust program that issues an HTTP GET request to `http://127.0.0.1:8000/dataset` to stream the FASTA data.
   - The FASTA headers are formatted as: `>sequence_id tm=<value>` (e.g., `>seq123 tm=62.4`).
   - The sequence body contains the primer nucleotides (A, C, G, T).

3. **Feature Extraction & Modeling (Rust):**
   - For each sequence, calculate two features:
     1. $L$: The length of the sequence (number of nucleotides).
     2. $GC$: The absolute count of 'G' and 'C' nucleotides in the sequence.
   - Fit a multiple linear regression model to predict $T_m$ based on $L$ and $GC$:
     $$T_m = \beta_0 + \beta_1 \cdot L + \beta_2 \cdot GC$$
   - You may use any Rust crates you need (e.g., `reqwest` for fetching, `nalgebra` or `linfa` for regression, or compute the least squares directly).

4. **Output:** 
   - Output the fitted model parameters to a JSON file exactly at `/home/user/model_weights.json`.
   - The JSON file must strictly have this format:
     ```json
     {
       "beta_0": 20.5,
       "beta_1": 0.52,
       "beta_2": 1.15
     }
     ```

Your final JSON file will be programmatically tested against a hidden holdout set of primers to verify the model's predictive accuracy.