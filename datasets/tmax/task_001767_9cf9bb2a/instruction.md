You are an MLOps engineer responsible for tracking experiment artifacts and setting up a new pipeline for analyzing embedding correlations using Bayesian inference. 

We use a custom, internal library called `bayes-metrics-tracker` for artifact logging and Bayesian covariance estimation. The source code for this package is currently vendored in your environment at `/app/bayes-metrics-tracker-1.2.0/`. However, the previous developer left the package in a broken state. 

Your tasks are to:
1. **Fix and Install the Vendored Package**:
   Navigate to `/app/bayes-metrics-tracker-1.2.0/`. There is a deliberate perturbation in the `setup.py` file that prevents installation (a hardcoded exception if a specific environment variable is not set, and a missing dependency). Identify and patch these issues so the package installs successfully in your Python environment.
   
2. **Compute Embeddings and Perform Correlation Analysis**:
   You have a dataset of sentences at `/home/user/data/sentences.csv`. 
   Write a Python script `/home/user/run_experiment.py` that:
   - Loads the dataset.
   - Computes text embeddings for each sentence using a pre-trained model (e.g., `sentence-transformers/all-MiniLM-L6-v2`).
   - Uses the `bayes_metrics_tracker.CovarianceEstimator` (from the package you just installed) to estimate the covariance matrix of the embedding dimensions.
   
3. **Cross-Validation and Hyperparameter Tuning**:
   The `CovarianceEstimator` takes a hyperparameter `prior_variance`. Use 5-fold cross-validation to tune this hyperparameter (search over `[0.1, 0.5, 1.0, 5.0]`) to minimize the negative log-likelihood on the validation folds. 
   
4. **Log Artifacts**:
   Use the `bayes_metrics_tracker.Logger` to save the best model artifact to `/home/user/artifacts/best_cov_matrix.npy`. Ensure the shape of this matrix matches `(embedding_dim, embedding_dim)`.

Your final pipeline must run successfully when executing `python /home/user/run_experiment.py` and produce the `/home/user/artifacts/best_cov_matrix.npy` file. The quality of your estimated covariance matrix will be evaluated against a hidden reference matrix. To pass, the Mean Squared Error (MSE) between your estimated covariance matrix and the reference matrix must be strictly less than 0.02.