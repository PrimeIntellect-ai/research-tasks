You are a data scientist tasked with cleaning a noisy dataset of high-dimensional embeddings. The dataset contains duplicates or near-duplicates that need to be removed to improve downstream model performance. You also need to track your experiment metrics and benchmark the similarity search performance under different numerical library configurations.

The raw dataset is located at: `/home/user/raw_embeddings.npy` (a NumPy array of shape `(5000, 512)` of type `float32`).

Your objective is to complete the following phases:

**Phase 1: Environment & Benchmarking**
1. Write a Python script to benchmark inference/similarity search performance.
2. Using the `faiss` library, build an `IndexFlatL2` index on the **raw** 512-dimensional dataset.
3. Query the index against itself (all 5000 vectors) to find the top 5 nearest neighbors (`k=5`).
4. Benchmark the time taken *only* for the query step (`index.search`).
5. Run this benchmark under two different thread configurations by setting the environment variable `OMP_NUM_THREADS` (which configures OpenMP/numerical library threads used by FAISS). Run it once with `OMP_NUM_THREADS=1` and once with `OMP_NUM_THREADS=4`. Record the query execution times (in seconds).

**Phase 2: Dimensionality Reduction**
1. Fit a Principal Component Analysis (PCA) model on the raw embeddings to reduce the dimensionality from 512 to 64. Use `scikit-learn`'s `PCA` with `random_state=42`.
2. Record the total explained variance ratio of these 64 components.

**Phase 3: Similarity Search & Cleaning**
1. Using the new 64-dimensional dataset, build a new `faiss.IndexFlatL2`.
2. Query the index against itself to find all pairs of vectors.
3. Identify all vectors that are "near-duplicates". A vector is considered a near-duplicate if it has an L2 distance strictly less than `1e-4` to another vector that appeared *earlier* in the dataset (i.e., has a smaller row index). 
4. Remove these near-duplicates to form a clean dataset. Retain the original order of the kept vectors.
5. Save the cleaned 512-dimensional vectors (using their original 512D representations, NOT the 64D ones) to `/home/user/clean_embeddings.npy`.

**Phase 4: Experiment Tracking**
1. Create an experiment tracking log file at `/home/user/experiment_results.json`. The JSON file must strictly contain the following keys and correct numerical values:
    * `"time_1_thread"`: Float, the time taken for the Phase 1 query with 1 thread.
    * `"time_4_threads"`: Float, the time taken for the Phase 1 query with 4 threads.
    * `"explained_variance_ratio_sum"`: Float, the sum of the explained variance ratio from Phase 2.
    * `"num_raw_vectors"`: Integer, the number of vectors in the raw dataset.
    * `"num_clean_vectors"`: Integer, the number of vectors in the cleaned dataset.

Ensure all dependencies (`numpy`, `scikit-learn`, `faiss-cpu`) are installed.