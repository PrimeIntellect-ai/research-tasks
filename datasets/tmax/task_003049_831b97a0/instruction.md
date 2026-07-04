You are an MLOps engineer responsible for building a lightweight, reproducible experiment tracking service in Rust. We have an audio artifact from a recent model run, and we need a microservice that ingests audio transcripts, computes a naive embedding (word counts), and uses a simple Bayesian model to track experiment success probability.

Here are your instructions:

1. **Audio Processing**:
   - There is an audio artifact located at `/app/artifact_091.wav`.
   - Transcribe this audio file. You may write a Python script using standard local tools (like `speech_recognition` with Sphinx, or any available lightweight transcriber you can install) to extract the text. 
   - Note the exact transcribed text, as you will need it to test your pipeline.

2. **Rust Tracking Service**:
   - Create a Rust HTTP server (using `axum`, `actix-web`, or `warp`) in `/home/user/mlops_tracker`.
   - The service must listen on `127.0.0.1:9090`.
   - The service must maintain an in-memory Bayesian tracking state for a single experiment metric: the "success rate" of our audio generation model. We use a Beta distribution initialized with $\alpha = 1.0$ and $\beta = 1.0$.

3. **API Endpoints**:
   The service must expose the following endpoints:
   
   - `POST /ingest`
     - Accepts a JSON payload: `{"transcript": "...", "artifact_id": "..."}`
     - **Schema Enforcement**: If either field is missing or empty, return HTTP 400.
     - **Embedding/Feature extraction**: Count the occurrences of the exact word "success" (case-insensitive) in the transcript.
     - **Bayesian Update**: If the word "success" appears 1 or more times, treat this as a successful trial (update $\alpha = \alpha + 1$). If it appears 0 times, treat it as a failed trial (update $\beta = \beta + 1$).
     - Returns HTTP 200 with JSON: `{"status": "ingested", "alpha": <new_alpha>, "beta": <new_beta>}`.
     
   - `GET /posterior`
     - Requires an authorization header: `Authorization: Bearer MLOPS_SECRET_2024`. If missing or incorrect, return HTTP 401.
     - Returns the expected value of the Beta distribution ($\frac{\alpha}{\alpha + \beta}$) as JSON: `{"expected_success_probability": <float>}`.

4. **Pipeline Reproducibility**:
   - To ensure your service works, manually (or via curl) submit the transcript of `/app/artifact_091.wav` to your `/ingest` endpoint with `artifact_id: "091"`. 
   - Leave the Rust server running in the background so our automated integration tests can verify its behavior across multiple protocol requests.