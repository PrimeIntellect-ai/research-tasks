You are an MLOps engineer tasked with optimizing the artifact retrieval system for our machine learning experiments. We use a custom C-accelerated Python package called `fastvec` to perform fast nearest-neighbor lookups on our model embedding artifacts.

Recently, our continuous integration pipeline started timing out because `fastvec` inference benchmarking is running much slower than expected. The source code for `fastvec` is vendored at `/app/fastvec-1.0/`. It seems a configuration error was introduced in its build setup during a recent refactor.

Your tasks are to:
1. **Fix and Install the Package**: Inspect the vendored package at `/app/fastvec-1.0/`, find and correct the build configuration that is causing the C-extension to compile without optimizations (it's currently running exceptionally slowly). Then, install the package in your environment.
2. **Process Artifacts**: 
   - You have 10 chunked numpy arrays containing reference model embeddings at `/home/user/data/ref_chunk_0.npy` through `/home/user/data/ref_chunk_9.npy`. Each chunk has shape `(10000, 512)`.
   - You have query embeddings at `/home/user/data/queries.npy` with shape `(1000, 512)`.
   - You have a PCA projection matrix at `/home/user/data/pca_matrix.npy` with shape `(128, 512)`.
   Load the chunks, concatenate them into a single reference array. 
   Project both the reference array and the query array into the 128-dimensional space using the PCA matrix. (Hint: $X_{proj} = X \times W^T$).
3. **Benchmark Inference**:
   Write a Python script at `/home/user/benchmark.py` that:
   - Initializes the fastvec index: `import fastvec; index = fastvec.Index(projected_refs)`
   - Measures the exact time taken to compute the top-5 nearest neighbors for all queries: `indices = index.query(projected_queries, k=5)`
   - Saves the results to `/home/user/benchmark_results.json` with the following structure:
     ```json
     {
       "inference_time_seconds": 0.123,
       "top_5_indices": [[...], [...]] // a list of lists containing the indices
     }
     ```

To pass this task, your output must be mathematically correct (the indices must match the exact nearest neighbors based on Euclidean distance) AND the `inference_time_seconds` must be strictly less than **0.25 seconds**. If you do not fix the package's build system, it will take over 2.0 seconds. Run your script to generate the final JSON file.