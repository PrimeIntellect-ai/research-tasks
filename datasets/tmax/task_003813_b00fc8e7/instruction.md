You are a Machine Learning Engineer working on a Rust-based semantic retrieval system. We have an existing codebase located in `/home/user/app/retrieval_system` that prepares training data, performs cross-validation to tune a similarity threshold, and serves the final model.

However, we have two major problems:
1. **Data Leakage in Cross-Validation:** The current ETL pipeline (`src/bin/etl.rs`) computes feature standardization (mean and standard deviation of embeddings) across the *entire* dataset before splitting it into K-folds. This data leak inflates our validation metrics. 
2. **Incomplete Serving Infrastructure:** The multi-service setup is partially broken, and the primary Rust server (`src/bin/server.rs`) needs to be configured and run to serve retrieval requests.

**Your Objectives:**

1. **Fix the Data Leak:**
   - Modify `/home/user/app/retrieval_system/src/bin/etl.rs` to compute the mean and standard deviation *only* on the training folds, and then apply those same parameters to standardize both the training and validation folds during cross-validation.
   - Run the ETL pipeline. It connects to a local mock embedding service. Once fixed, the pipeline will output the correct tuned threshold.
   - Save the newly tuned, correct threshold (a single float value) into a file at `/home/user/app/best_hyperparameter.txt`.

2. **Establish the Multi-Service Environment:**
   - In `/home/user/app/`, there is a startup script `start_services.sh` that launches the auxiliary services (a mock Embedding Service on port 9000 and a mock Data Service on port 9001).
   - Ensure these services are running.

3. **Deploy the Serving API:**
   - Complete and launch the main Rust retrieval API (`src/bin/server.rs`).
   - The server MUST listen on `127.0.0.1:8080`.
   - It must expose a `POST /retrieve` endpoint.
   - The endpoint must accept requests with an Authorization header exactly matching: `Authorization: Bearer ds_secret_token`.
   - The JSON request payload will be of the form: `{"query": "example text"}`.
   - The server must fetch the embedding from the Embedding Service (`http://127.0.0.1:9000/embed`), standardize it using the global mean and std derived from the *entire* dataset (since this is production inference now), and return the closest matching document ID from the Data Service (`http://127.0.0.1:9001/data`) that meets the tuned threshold.
   - The response must be a JSON object: `{"match_id": "doc_xyz", "confidence": 0.88}`. If no documents meet the threshold, return `{"match_id": null, "confidence": 0.0}`.

**Constraints:**
- Use Rust (cargo) for compiling and running the binaries. 
- You may use standard Unix utilities alongside it.
- Do not change the auxiliary service scripts, only the Rust codebase.