You are an AI assistant helping a data science researcher build an automated system to organize and score the quality of various datasets using Bayesian inference. The researcher relies on a specialized, high-performance Bayesian inference package, but the setup is currently broken, and the full pipeline needs to be implemented.

Your task consists of three main phases:

**Phase 1: Fix and Install the Vendored Package**
The researcher uses a custom Python C-extension/Cython package called `fast_bayes` located at `/app/vendored/fast_bayes`. 
Currently, attempting to build and install this package (e.g., via `pip install -e .`) fails because its `setup.py` has a deliberate misconfiguration. Specifically, the package uses NumPy C-APIs, but the `setup.py` fails to properly import NumPy and include its C-header directories.
1. Fix the `/app/vendored/fast_bayes/setup.py` file.
2. Successfully install the `fast_bayes` package into the current Python environment.

**Phase 2: Cross-Validation and Reproducibility**
The researcher has provided a dataset of meta-features at `/home/user/data/metrics.csv`. The first 4 columns are numerical features (X), and the 5th column is a binary target (y) indicating high (1) or low (0) dataset quality.
1. Use the `fast_bayes.BayesianClassifier` from the newly installed package.
2. Write a Python script to perform a 5-fold cross-validation on this dataset to tune the hyperparameter `alpha` (prior variance). Test the values `alpha = [0.1, 1.0, 10.0]`. Ensure your splits are reproducible by setting a random seed of `42`.
3. Output the single best `alpha` value to a file at `/home/user/best_alpha.txt`.

**Phase 3: Serve the Model for Inference Performance Benchmarking**
The researcher needs a reproducible way to evaluate dataset quality over the network while benchmarking inference times.
1. Write and start a Python web server (using Flask, FastAPI, or standard library HTTP) that listens on `127.0.0.1:8080`.
2. The server must expose an endpoint: `POST /evaluate`.
3. The endpoint must require a bearer token for authentication. The client will send the header: `Authorization: Bearer ds-research-2024`. If missing or incorrect, return a 401 Unauthorized status.
4. The endpoint expects a JSON payload containing an array of 4 floats: `{"features": [1.5, 2.1, 0.4, 3.2]}`.
5. The server must use the `fast_bayes.BayesianClassifier` initialized with the *best* `alpha` found in Phase 2, fitted on the entire `/home/user/data/metrics.csv` dataset.
6. The server must measure the exact wall-clock time it takes to run the `.predict_proba(features)` method.
7. Return a JSON response exactly matching this structure:
   `{"quality_score": <float>, "inference_time_ms": <float>}`
   Where `quality_score` is the probability of class 1 returned by the model, and `inference_time_ms` is the prediction time converted to milliseconds.

Leave the server running in the background so it can be automatically verified.