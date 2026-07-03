You are an MLOps engineer optimizing a vector retrieval system for a production application. To reduce memory footprint and latency, you are investigating whether applying Principal Component Analysis (PCA) to the dense text embeddings can maintain high retrieval accuracy while shrinking the embedding size.

Your environment contains the following files:
- `/home/user/data/corpus_embeddings.npy`: A NumPy array of shape `(5000, 384)` representing the dense embeddings of a document corpus.
- `/home/user/data/query_embeddings.npy`: A NumPy array of shape `(100, 384)` representing the dense embeddings of 100 search queries.

Your task is to implement an evaluation script in Python that performs the following:

1. **Baseline Retrieval:**
   - Compute the ground-truth Top-10 nearest neighbors from the corpus for each query using **Cosine Similarity**.
   - Store these indices as the baseline for accuracy computation.

2. **Dimensionality Reduction & Hyperparameter Tuning:**
   - Evaluate the following candidate dimensions for PCA `n_components`: `[16, 32, 64, 128]`.
   - For each candidate dimension:
     - Initialize `sklearn.decomposition.PCA` with the candidate `n_components` and `random_state=42`.
     - Fit the PCA model on the `corpus_embeddings` and transform both the corpus and the queries.
     - Compute the Top-10 nearest neighbors for each query using the PCA-reduced embeddings (again, using Cosine Similarity).
     - Calculate the **Recall@10** for each query: the fraction of the baseline ground-truth Top-10 indices that are also present in the PCA-reduced Top-10 indices.
     - Compute the average Recall@10 across all 100 queries.
   - Select the **smallest** `n_components` from the candidate list that achieves an **average Recall@10 >= 0.85**.

3. **Inference Performance Benchmarking:**
   - Using the `time` module, measure the total time taken to compute the Cosine Similarity matrix and find the Top-10 neighbors for all 100 queries against the 5000 corpus vectors.
   - Do this once for the **raw embeddings** (384 dimensions) and once for the **optimal PCA-reduced embeddings** found in step 2.

4. **Reporting:**
   - Generate a JSON report at `/home/user/report.json` exactly matching this structure:
     ```json
     {
         "baseline_shape": [5000, 384],
         "optimal_n_components": <integer>,
         "optimal_recall_at_10": <float, rounded to 4 decimal places>,
         "latency_raw_seconds": <float>,
         "latency_optimal_seconds": <float>
     }
     ```

**Constraints & Notes:**
- You must use Python and the `numpy`, `scikit-learn`, and `scipy` libraries. You may install `scikit-learn` and `scipy` if they are missing.
- When computing top-10, sort the top 10 elements by similarity in descending order (or distance in ascending order). If there are ties, `numpy`'s default argsort behavior is acceptable.
- Ensure all directories and files are written to the exact specified paths.