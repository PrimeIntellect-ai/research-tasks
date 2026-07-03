You are an ML Engineer preparing training data and deploying a highly optimized inference service. You have been given a proprietary, compiled legacy feature extractor that produces high-dimensional embeddings from raw log data. Your goal is to process the data, train a computationally efficient model using dimensionality reduction, and deploy it as an API.

Follow these steps exactly:

1. **Environment Setup**
   Set up your Python environment in `/home/user/env`. You will need to install the necessary libraries for data science, machine learning, and running an HTTP API (e.g., scikit-learn, pandas, fastapi, uvicorn).

2. **Data Generation with Legacy Binary**
   We have a stripped binary at `/app/log_embedder`. This tool takes a JSON file containing a list of text logs and outputs a CSV file of high-dimensional embeddings (1024 dimensions, no header).
   Run the tool on the raw logs provided at `/home/user/logs.json` and save the output to `/home/user/embeddings.csv`.
   Usage: `/app/log_embedder -i /home/user/logs.json -o /home/user/embeddings.csv`

3. **Dimensionality Reduction & Cross-Validation**
   The labels for the logs are provided in `/home/user/labels.json` (a flat JSON array of integers, either 0 or 1, in the exact same order as the logs).
   The 1024-D embeddings are too slow for our real-time inference constraints. Write a Python script `/home/user/train.py` to train a scikit-learn pipeline consisting of `PCA` followed by a `LogisticRegression` classifier.
   Use 5-fold cross-validation to perform hyperparameter tuning to find the configuration that maximizes **Accuracy**. Search the following parameter grid:
   - PCA `n_components`: [16, 32, 64]
   - LogisticRegression `C`: [0.1, 1.0, 10.0]
   Save the best pipeline (the fully fitted PCA and LogisticRegression model) to `/home/user/best_pipeline.pkl`.

4. **Inference Performance Benchmarking & API Deployment**
   Create and start an HTTP service `/home/user/server.py` that listens on `127.0.0.1:8080`.
   The service must expose a single endpoint:
   `POST /score`
   Request Body (JSON):
   ```json
   {
     "raw_embedding": [0.12, -0.45, ...] // A list of 1024 floats
   }
   ```
   Response (JSON):
   ```json
   {
     "class": 1, // or 0
     "inference_time_ms": 1.25 // The time taken to run PCA + predict on this single vector, in milliseconds
   }
   ```
   
Your service must remain running in the background on `127.0.0.1:8080` so that automated tests can verify its behavior. Wait until the service is fully started before completing your turn.