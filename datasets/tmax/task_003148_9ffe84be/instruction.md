You are an AI assistant helping a machine learning researcher organize and benchmark dataset operations. 

The researcher has generated a large set of document embeddings distributed across several HDF5 files in the directory `/home/user/data/`. There are 5 files named `docs_0.h5` through `docs_4.h5`. Each file contains a dataset named `embeddings` with shape (2000, 256) of type float32.
There is also a file `/home/user/queries.h5` containing a dataset `queries` with shape (100, 256) of type float32.

Your task is to implement an experiment tracking and benchmarking pipeline that computes the cosine similarity between the queries and all documents, using two different methods to verify numerical accuracy and measure inference performance.

Step 1: Write a Python script `/home/user/search.py` that:
- Loads the queries.
- Loads and concatenates all document embeddings from the 5 HDF5 files in order (0 to 4) to form a single matrix of shape (10000, 256).
- Implements a `naive_search` function that computes the cosine similarity matrix (shape 100 x 10000) using nested Python loops (looping over queries and documents, calculating the dot product divided by the product of L2 norms). Time this function.
- Implements an `optimized_search` function that computes the same cosine similarity matrix using fully vectorized NumPy matrix operations (linear algebra) without any loops over the queries or documents. Time this function.
- Computes the maximum absolute difference between the similarity matrices produced by the two methods (Numerical accuracy testing).
- Finds the indices of the top 5 most similar documents for each query using the optimized similarity matrix.

Step 2: The Python script must output the benchmarking results and tracked metrics to a JSON file at `/home/user/metrics.json` with the following exact keys:
- `"max_abs_error"`: (float) the maximum absolute difference between the naive and optimized similarity matrices.
- `"naive_time_sec"`: (float) execution time of `naive_search` in seconds.
- `"optimized_time_sec"`: (float) execution time of `optimized_search` in seconds.
- `"speedup"`: (float) `naive_time_sec / optimized_time_sec`.
- `"top_5_indices"`: (list of lists of ints) for each of the 100 queries, the indices (0 to 9999) of the top 5 documents with the highest cosine similarity.

Step 3: Write a shell script `/home/user/run_experiment.sh` that installs any necessary system or Python dependencies (e.g., `h5py`, `numpy`), runs the Python script, and prints "Experiment completed successfully" to stdout. Make sure the script is executable.

Constraints:
- Do not use ML frameworks like PyTorch or TensorFlow; strictly use NumPy and standard Python libraries for the math.
- Ensure the `run_experiment.sh` script exits with code 0.